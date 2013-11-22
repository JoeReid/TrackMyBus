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
    
    # Validation
    for field in ['bus_id','route_id','lon', 'lat']:
        if not request.params.get(field):
            raise action_error(message='no {0}'.format(field), code=400)

    # Convert input types
    request.params['bus_id'] = int  (request.params['bus_id'])
    request.params['lon']    = float(request.params['lon'])
    request.params['lat']    = float(request.params['lat'])

    # Record bus position
    bus_position = BusPosition()
    for field, value in request.params.items():
        try   : setattr(bus_position,field,value)
        except: pass
    DBSession.add(bus_position)

    # Record checkin - (register a bus at a busstop with timestamp if it is within threshold distance)
    th = request.registry.settings.get('bus.checkin.threshold')
    try:
        (bus_stop_id, ) = DBSession.query(BusStop.id) \
            .filter(BusStop.lon>request.params['lon']-th) \
            .filter(BusStop.lon<request.params['lon']+th) \
            .filter(BusStop.lat>request.params['lat']-th) \
            .filter(BusStop.lat<request.params['lat']+th) \
            .limit(1).one()
        bus_checkin = BusCheckin()
        bus_checkin.bus_id = request.params['bus_id']
        bus_checkin.bus_stop_id = bus_stop_id
        DBSession.add(bus_checkin)
    except NoResultFound:
        pass

    return action_ok(data={})

@view_config(route_name='position') # Could have get router here for REST
@web
def position_get(request):
    """
    For a bus number, get the last positions
    This could be drawn as a path on a map
    """
    return action_ok(data={})

@view_config(route_name='checkin')
@web
def last_checkin(request):
    """
    Get the last recorded bus checkin for this bus
    """
    return action_ok(data={})
