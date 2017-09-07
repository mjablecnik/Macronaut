#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Macro library
  
"""

import os, sys
from time import sleep, time
import keylogger
import ast

SCRIPT_PATH = os.path.dirname(sys.argv[0])

TMP_PATH = '/tmp/macro-creator'
TMP_DIR = TMP_PATH + '/keyrec/' 
STOP_FILE = TMP_PATH + '/stop-rec'   # if doesn't exist so recording is stopped

OUTPUT_PATH = SCRIPT_PATH + '/tmp/macro/'

RAW_FILE = TMP_DIR + 'macro-data'

keystate = {
     'left ctrl': False,
     'left alt': False,
     'left shift': False,
     'right ctrl': False,
     'right alt': False,
     'right shift': False,
}


def record(raw_file):
    file = open(raw_file, 'w')
    def print_keys(t, modifiers, keys): 
        text_format = ("%.2f|%r|%r\n" % (t, keys, modifiers))
        file.write(text_format)
        print(text_format)


    while os.path.isfile(STOP_FILE):
        sleep(.005)
        changed, modifiers, keys = keylogger.fetch_keys()
        if keys == 'q':
            os.system("rm %s" % (STOP_FILE,))

        if changed: 
            print_keys(time(), modifiers, keys)

    file.close()


def parse_data(lines):
    events = []
    event = 0
    for line in lines:
        event += 1
        keys = line.split('|')
        key = keys[1]
        keystate = ast.literal_eval(keys[2])
        if key != 'None': 
            key = key[1:-1]
            events.append([key, keystate])
    return events


# check if hotkey is pressed
def is_hotkey(event):
    hotkeys = event[1]
    for hotkey, value in hotkeys.items():
        if value:                                # if hotkey is pressed
            return True
    return False

# generating of macro code
def compile(raw_data):
    events = parse_data(raw_data)
    text = ''
    hotkey_str = ''
    for event in events:
        if is_hotkey(event):
            hotkeys = event[1]
            hotkey_str = "hotkey('"
            for hotkey, value in hotkeys.items():
                if value:                                # if hotkey is pressed
                     hotkey_str += hotkey.split(' ')[1]  #add name of key
                     hotkey_str += "', '"
            hotkey_str += "%s')\n" % event[0]
            text += hotkey_str
        else:
            key = event[0]
            if key == '<enter>':
                text += "typewrite(['enter'])\n"
            elif key == '<tab>':
                text += "typewrite(['tab'])\n"
            elif key == '<caps lock>':
                text += "typewrite(['esc'])\n"
            else:
                text += "typewrite('%s')\n" % key 

    return text





def save(text, name='macro-output.py', macro_path='/tmp/macro/'):
    file = open(macro_path+'/'+name, 'w')

    head = """#!/usr/bin/env python

from pyautogui import hotkey, typewrite, click
from time import sleep
sleep(0.5)
"""
    file.write(head+text)
    file.close()

