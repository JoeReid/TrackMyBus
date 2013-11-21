from . import Base

from sqlalchemy     import Column, ForeignKey
from sqlalchemy     import Unicode, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session
from sqlalchemy.orm.exc import NoResultFound

import copy

import datetime
now = lambda: datetime.datetime.now()


__all__ = [
    'BusPosition',
    'BusStop',
    'BusCheckin',
]


class BusPosition(Base):
    """
    """
    __tablename__   = "bus_position"

    id              = Column(Integer() , primary_key=True)    
    route_id        = Column(Unicode(4), nullable=False)
    timestamp       = Column(DateTime(), nullable=False, default=now)
    lat             = Column(Float()   , nullable=False)
    lon             = Column(Float()   , nullable=False)
    
    @staticmethod
    def last_position(DBSession, route_id):
        """
        """
        try:
            return DBSession.query(BusPosition).order_by(BusPosition.timestamp.desc()).limit(1).one()
        except NoResultFound:
            return None
    
    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'route_id'    : None ,
            'timestamp'   : None ,
            'lat'         : None ,
            'lon'         : None ,
        },
    })    
    __to_dict__.update({'full': copy.deepcopy(__to_dict__['default'])})
    __to_dict__['full'].update({
    })


class BusStop(Base):
    """
    """
    __tablename__   = "bus_stop"

    id              = Column(Integer() , primary_key=True)
    route_id        = Column(Unicode(4), nullable=False)
    lat             = Column(Float()   , nullable=False)
    lon             = Column(Float()   , nullable=False)

    @property
    def last_checkin(self):
        """
        Not good form to have querying in models
        Could this be eager loaded?
        """
        try:
            (timestamp,) = object_session(self).query(BusCheckin.timestamp) \
                            .filter(BusCheckin.bus_stop_id==self.id) \
                            .order_by(BusCheckin.timestamp.desc()) \
                            .limit(1).one()
            return timestamp
        except NoResultFound:
            return None

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'route_id'    : None ,
            'lat'         : None ,
            'lon'         : None ,
        },
    })    
    __to_dict__.update({'full': copy.deepcopy(__to_dict__['default'])})
    __to_dict__['full'].update({
        'last_checkin'    : None , 
    })


class BusCheckin(Base):
    """
    """
    __tablename__   = "bus_checkin"
    id              = Column(Integer() , primary_key=True)
    bus_stop_id     = Column(Integer() , ForeignKey('bus_stop.id'), nullable=False)
    timestamp       = Column(DateTime(), nullable=False, default=now)
    
    bus_stop        = relationship("BusStop")

    __to_dict__ = copy.deepcopy(Base.__to_dict__)
    __to_dict__.update({
        'default': {
            'route_id'    : lambda bus_checkin: bus_checkin.bus_stop.route_id,
            'lat'         : lambda bus_checkin: bus_checkin.bus_stop.lat,
            'lon'         : lambda bus_checkin: bus_checkin.bus_stop.lon,
            'timestamp'   : None ,
        },
    })    
    __to_dict__.update({'full': copy.deepcopy(__to_dict__['default'])})
    __to_dict__['full'].update({
    })
