# coding=utf-8
import platform
import locale
import logging
import hashlib
import requests

from .robart import *

def scan(network, port=10009):
    list = []
    
    rest = robart.Robart_REST(network, port)
    rest.set_rest_timeout(0.05, 1)
    pieces = network.split('.')
    if len(pieces) == 4:
        net = "{}.{}.{}".format(pieces[0], pieces[1], pieces[2])
        for a in range(1, 255):
            i = "{}.{}".format(net, a)
            try:
                rest.set_rest_url(i, port)
                if rest.call_rest('get/robot_id') != False:
                    list.append(i)
            except:
                pass
    return list


#adding a new "trace" log level
TRACE_LEVEL_NUM = 5 
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws) 
logging.Logger.trace = trace
