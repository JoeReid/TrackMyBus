# Imports
import time
import socket
import json
import gps

# Global vars
gRoute = ""
gLatLong = ""


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
        pass
    