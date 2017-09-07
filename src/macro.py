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
import config


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


    while os.path.isfile(config.STOP_FILE):
        sleep(.005)
        changed, modifiers, keys = keylogger.fetch_keys()
        if keys == 'q':
            os.system("rm %s" % (config.STOP_FILE,))

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
def compile(raw_data, file):
    events = parse_data(raw_data)
    text = ''
    hotkey_str = ''
    for event in events:
        if is_hotkey(event):
            hotkeys = event[1]
            hotkey_str = "xdotool key "
            for hotkey, value in hotkeys.items():
                if value:                                # if hotkey is pressed
                     hotkey_str += hotkey.split(' ')[1]  #add name of key
                     hotkey_str += "+"
            hotkey_str += "%s\n" % event[0]
            text += hotkey_str
        else:
            key = event[0]
            if key == '<enter>':
                text += "xdotool key Return\n"
            elif key == '<tab>':
                text += "xdotool key Tab\n"
            elif key == '<caps lock>':
                text += "xdotool key Escape\n"
            else:
                text += "xdotool key %s\n" % key 

    file = open(file, 'w')
    file.write(text)
    file.close()







