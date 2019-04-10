# coding=utf-8

import platform 
import locale 
import logging 
import hashlib 

import requests
import json
from builtins import range
import sys

import logging
_LOGGER = logging.getLogger(__name__)


class Robart_REST(object):
    """This class represents a generic object to make basic requests to the robot"""
    _restCallHeaders = {'content-type': 'http/1.1', 'accept': 'application/json'}
    _restCallRequestCounter = 3 
    _restCallTimout = 3
    _restCallUrl = ''
    
    def set_rest_timeout(self, timeout=3, counter=3):
        self._restCallTimout = timeout
        self._restCallRequestCounter = counter 

    def set_rest_url(self, ip, port=10009):
        self._restCallUrl = "http://{}:{}".format(ip, port)
    
    def __init__(self, ip, port=10009):
        self.set_rest_url(ip, port)
    
    def call_rest(self, path, body = None):
        result = None
        requestPath =  "{}/{}".format(self._restCallUrl, path)
        for i in range(0,self._restCallRequestCounter):
            try:
                result = requests.get(requestPath, data=body, headers=self._restCallHeaders, timeout=self._restCallTimout)
                ret = (result.json() if result.content != "" else "")
                return ret
            except requests.Timeout:
                pass
        return False

    def from_json(self, js):
        pass

    def __repr__(self):
        return "id({}) {}".format(self.id,self.__str__())

    def __unicode__(self):
        return u'id({})'.format(self.id)

    def __str__(self):
        if sys.version_info >= (3,0):
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')
            
            
            
class Robart_MyVacBot(Robart_REST):
    _name = None
    _unique_id = None
    _camlas_unique_id = None
    _model = None
    _firmware = None
    
    _mode = None
    _charging = None
    _battery_level = None
    _voltage = None
    _cleaning_parameter_set = None
    _time = None
    

    def __init__(self, ip, port='10009'):
        try:
            if self.call_rest('get/robot_id') == False:
                print("scan")
        except:
            None
        super().__init__(ip, port)
                
    def from_json_id(self, js):
        super().from_json(js)
        self._name = js["name"]
        self._unique_id = js["unique_id"]
        self._camlas_unique_id = js["camlas_unique_id"]
        self._model = js["model"]
        self._firmware = js["firmware"]

    def from_json(self, js):
        super().from_json(js)
        self._mode = js["mode"]
        self._charging = js["charging"]         
        self._battery_level = js["battery_level"]
        self._voltage = js["voltage"] / 1000
        self._cleaning_parameter_set = js["cleaning_parameter_set"]
        self._time = js["time"]        
    
    def get_robotid(self):
        json_state = self.call_rest('get/robot_id')
        self.from_json_id(json_state)
        return True
        
    def get_state(self):
        json_state = self.call_rest('get/status')
        self.from_json(json_state)
        return True
    
    def set_home(self):
        json_state = self.call_rest('set/go_home')
    
    def set_stop(self):
        json_state = self.call_rest('set/stop')
    
    def set_clean(self):
        json_state = self.call_rest('set/clean_start_or_continue?cleaning_parameter_set=1')

    def test(self, arg):
        json_state = self.call_rest(arg)
