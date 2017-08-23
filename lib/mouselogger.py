#!/usr/bin/python

import logging
from socket import gethostname
from pymouse import PyMouse
import random
import time
from signal import signal, SIGINT
daemon = True



from pymouse import PyMouseEvent

class event(PyMouseEvent):
    def __init__(self):
        super(event, self).__init__()
        FORMAT = '%(asctime)-15s ' + gethostname() + ' touchlogger %(levelname)s %(message)s'
        logging.basicConfig(filename='mouse.log', level=logging.DEBUG, format=FORMAT)

    def move(self, x, y):
        pass

    def click(self, x, y, button, press):
        if press:
            logging.info('{ "event": "click", "type": "press", "button":'+ str(button) +', "x": "' + str(x) + '", "y": "' + str(y) + '"}')
        else:
            logging.info('{ "event": "click", "type": "release", "button":'+ str(button) +', "x": "' + str(x) + '", "y": "' + str(y) + '"}')

e = event()
e.capture = False
e.daemon = False
e.start()

