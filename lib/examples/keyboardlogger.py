#!/usr/bin/python

import logging
from socket import gethostname
from pykeyboard.x11 import PyKeyboardEvent
import random
import time
from signal import signal, SIGINT
from Xlib.protocol import rq
daemon = True



from pymouse import PyMouseEvent

class event(PyKeyboardEvent):
    def __init__(self):
        super(event, self).__init__()

    def tap(self, keycode, character, press):
        print keycode, character, press

e = event()
e.capture = False
e.daemon = False
e.run()

