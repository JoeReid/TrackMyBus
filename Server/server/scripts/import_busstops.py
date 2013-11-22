"""
External dependencys do not be commited to the repo
"""
import os
import csv
import re

from ..model.model_bus import BusStop
from ..model           import init_DBSession, DBSession, commit


import logging
log = logging.getLogger(__name__)


#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

VERSION = "0.0"
DEFAULT_INPUT_FILENAME = 'data/Stops.csv'
DEFAULT_FILTER_BOUNDS = '0.6,51.0:1.5,51.5' #lon,lat:lon,lat


#canterbury 1.07123	51.28497
#ramsgate 1.43258	51.34918
#sittingbourne 0.71494	51.35101

class FilterBounds():
    
    def __init__(self, filter_bounds_str):
        lon1, lat1, lon2, lat2 = map(float, re.match(r'(?P<lon1>[\d\.]+),(?P<lat1>[\d\.]+):(?P<lon2>[\d\.]+),(?P<lat2>[\d\.]+)',filter_bounds_str).groups())
        self.left = min(lon1,lon2)
        self.right = max(lon1,lon2)
        self.top = min(lat1,lat2)
        self.bottom = max(lat1,lat2)

    def in_bounds(self, *args):
        """
        lon,lat or str 'lon,lat'
        """
        if len(args)==1 and isinstance(args[0], str):
            lon, lat = map(float, re.match(r'([\d\.]+),([\d\.]+)',args[0]).groups())
        elif len(args)==2:
            try:
                lon, lat = float(args[0]), float(args[1])
            except Exception:
                return False
        else:
            return
        if lon>self.left and lon<self.right and lat>self.top and lat<self.bottom:
            return True



#-------------------------------------------------------------------------------
# CSV importer
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
# Command Line
#-------------------------------------------------------------------------------

def get_args():
    import argparse
    # Command line argument handling
    parser = argparse.ArgumentParser(
        description="""Download dependencys""",
        epilog=""""""
    )
    parser.add_argument('-i','--csv_input', help='csv input', default=DEFAULT_INPUT_FILENAME)
    parser.add_argument('--config_uri', help='config .ini file for db settings', default='development.ini')
    parser.add_argument('--filter_bounds', help='two co-ordinate to import bus stops from', default=DEFAULT_FILTER_BOUNDS)
    parser.add_argument('--version', action='version', version=VERSION)

    return parser.parse_args()

def main():
    args = get_args()
    
    # Setup Logging and Db from .ini
    from pyramid.paster import get_appsettings, setup_logging
    #setup_logging(args.config_uri)
    logging.basicConfig(level=logging.INFO)
    settings = get_appsettings(args.config_uri)
    init_DBSession(settings)

    filter_bounds = FilterBounds(args.filter_bounds)

    with open(args.csv_input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        count = 0
        for row in csv_reader:
            id, name, direction, lon, lat = [row[i] for i in [1,4,16,29,30]]
            if filter_bounds.in_bounds(lon, lat):
                busstop = BusStop()
                if id:
                    busstop.id = id
                busstop.name = name
                busstop.direction = direction
                busstop.lon = lon
                busstop.lat = lat
                DBSession.add(busstop)
                commit()
                print(id, name, direction, lon, lat)
            count += 1
            if count % 100000 == 0:
                print('Processed: {0}'.format(count))

    
if __name__ == "__main__":
    main()