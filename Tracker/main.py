# Imports
import time
import socket
import json
import threading
from gps import *

# Global vars
gRoute = ""
gLatLong = ""
gpsd = None
# use gpsd.fix.latitude and gpsd.fix.longitude
# also gpsd.fix.mode for determining fix


class dataObject(object):
    def __init__(self, ip, port):
        self.timestamp = time.time()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
    
    def updateTime(self):
        self.timestamp = time.time()
    
    def formatJson(self):
        data = {'routeNumber': gRoute, 'latLong':gLatLong, 'timeStamp':self.timeStamp}
        return json.dumps(data)
    
    def send(self):
        self.updateTime()
        self.s.connect(self.ip, self.port)
        self.s.send(self.formatJson())
    
class dataListener(object):
    def __init__(self):
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.running = False
        
    # to be run in a thread
    def run(self):
        self.running = True
        while self.running:
            self.gpsd.next()
    
    def stop(self):
        self.running = False
    
def main():
    l = dataListener()
    d = dataObject()
    

main()