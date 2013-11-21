"""
Init base tables
This should by convention be separate to the DBSession as this imports Model objects
and therefore binding to Base
"""

from . import DBSession, init_db, commit


import logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# DB Objects
#-------------------------------------------------------------------------------

# The DB modules imported here will be created as part of the blank database.
# If you add a new model ensure it ia added here
from .model_bus   import BusCheckin, BusStop, BusPosition


#-------------------------------------------------------------------------------
# Init Base Data
#-------------------------------------------------------------------------------

def init_data():
    init_db() # Clear current DB and Create Blank Tables
    
    log.info("Populating tables with base data")
    

    commit()  # Can't simply call DBSession.commit() as this is han handled my the Zope transcation manager .. wha?!

    