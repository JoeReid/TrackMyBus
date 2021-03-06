import datetime

from pyramid.view import view_config

from ..lib.misc import setattrs

from . import web
from ..lib.auto_format    import action_ok, action_error

from ..model              import DBSession, commit
from ..model.model_bus    import BusStop, BusCheckin, BusPosition
from sqlalchemy.orm.exc import NoResultFound

import logging
log = logging.getLogger(__name__)


@view_config(route_name='position_update') # Could have put router here for REST
@web
def position_update(request):
    """
    Update a bus location and checkin to nearbu stop
    """
    params = dict(request.params)
    # Validation
    for field in ['bus_id','route_id','lon', 'lat']:
        if not params.get(field):
            raise action_error(message='no {0}'.format(field), code=400)

    # Convert input types
    params['bus_id'] = int  (params['bus_id'])
    params['lon']    = float(params['lon'])
    params['lat']    = float(params['lat'])

    # Record bus position
    bus_position = BusPosition()
    for field, value in params.items():
        try   : setattr(bus_position,field,value)
        except: pass
    DBSession.add(bus_position)

    # Record checkin - (register a bus at a busstop with timestamp if it is within threshold distance)
    th = request.registry.settings.get('bus.checkin.threshold')
    try:
        (bus_stop_id, ) = DBSession.query(BusStop.id) \
            .filter(BusStop.lon>params['lon']-th) \
            .filter(BusStop.lon<params['lon']+th) \
            .filter(BusStop.lat>params['lat']-th) \
            .filter(BusStop.lat<params['lat']+th) \
            .limit(1).one()
        bus_checkin = BusCheckin()
        bus_checkin.bus_id = params['bus_id']
        bus_checkin.bus_stop_id = bus_stop_id
        DBSession.add(bus_checkin)
    except NoResultFound:
        pass

    return action_ok(data={})


@view_config(route_name='position_get') # Could have get router here for REST
@web
def position_get(request):
    """
    For a bus number, get the last positions
    This could be drawn as a path on a map
    """
    params = dict(request.params)
    try:
        params['bus_id'] = int(params['bus_id'])
    except (KeyError, ):
        raise action_error(message='no {0}'.format('bus_id'), code=400)
    
    positions = DBSession.query(BusPosition) \
        .filter(BusPosition.bus_id==params['bus_id']) \
        .order_by(BusPosition.timestamp) \
        .limit(params.get('count',request.registry.settings.get('bus.api.positions.count.default'))) \
        .all()
    return action_ok(
        data={
            "type": "FeatureCollection",
            'features': [pos.to_dict() for pos in positions],
        }
    )


@view_config(route_name='last_checkin')
@web
def last_checkin(request):
    """
    Get the last recorded bus checkin for this bus
    """
    return action_ok(data={})


@view_config(route_name='near_stops')
@web
def near_stops(request):
    params = dict(request.params)
    # Validation
    #for field in ['lon', 'lat']:
    #    if not params.get(field):
    #        raise action_error(message='no {0}'.format(field), code=400)

    # Convert input types
    params['bbox'] = [float(n) for n in params['bbox'].split(",")]

    bus_stops_all = DBSession.query(BusStop) \
        .limit(500).all()
        #.limit(50).all()
#        .filter(BusPosition.lon>params['bbox'][0]) \
#        .filter(BusPosition.lon<params['bbox'][2]) \
#        .filter(BusPosition.lat>params['bbox'][1]) \
#        .filter(BusPosition.lat<params['bbox'][3]) \

    bus_stops = []

    for bus in bus_stops_all:
        print(bus.lon, params['bbox'][0], params['bbox'][2])
        print(bus.lat, params['bbox'][1], params['bbox'][3])
        if (
            bus.lon > params['bbox'][0] and bus.lon < params['bbox'][2] and
            bus.lat > params['bbox'][1] and bus.lat < params['bbox'][3]
        ):
            bus_stops.append(bus)
    
    print("stops: %d " % len(bus_stops))
    return action_ok(data={
        "type": "FeatureCollection",
        "features": [bus_stop.to_dict() for bus_stop in bus_stops]
    })


@view_config(route_name='near_bus')
@web
def near_bus(request):
    params = dict(request.params)
    # Validation
    #for field in ['lon', 'lat']:
    #    if not params.get(field):
    #        raise action_error(message='no {0}'.format(field), code=400)
    params['bbox'] = [float(n) for n in params['bbox'].split(",")]

    bus_positions = DBSession.query(BusPosition) \
        .filter(BusPosition.timestamp>datetime.datetime.now()-datetime.timedelta(minutes=15)) \
        .order_by(BusPosition.timestamp) \
        .all()
#        .filter(BusPosition.lon>params['bbox'][0]) \
#        .filter(BusPosition.lon<params['bbox'][2]) \
#        .filter(BusPosition.lat>params['bbox'][1]) \
#        .filter(BusPosition.lat<params['bbox'][3]) \
        # group_by needs all columns to be explicit
        #.limit(10).all()
        #.group_by(BusPosition.bus_id) \

    # get the latest update for each bus in the area
    latest = {}
    for pos in bus_positions:
        if pos.bus_id not in latest or latest[pos.bus_id].timestamp < pos.timestamp:
            latest[pos.bus_id] = pos

    print("Busses %d" % len(latest))
    return action_ok(data={
        "type": "FeatureCollection",
        "features": [bus_position.to_dict() for bus_position in latest.values()]
    })
