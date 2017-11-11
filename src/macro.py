#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Program for generating automatic scripts.
  
"""

import os, sys
from time import sleep, time
import keylogger
import ast
import config
from pynput import mouse, keyboard
import threading


keystate = {
     'left ctrl': False,
     'left alt': False,
     'left shift': False,
     'right ctrl': False,
     'right alt': False,
     'right shift': False,
}


def record(raw_file):
    f = open(raw_file, 'w')
    f.close()
    f = open(raw_file, 'a')

    def on_press(key):
        f.write( 'keyboard|press|{0}\n'.format(key) )
        print( 'keyboard|press|{0}\n'.format(key) )

    def on_release(key):
        f.write( 'keyboard|release|{0}\n'.format(key) )
        print( 'keyboard|release|{0}\n'.format(key) )
        if key == keyboard.Key.esc:
            # Stop listener
            return False


    t1 = keyboard.Listener(on_press=on_press, on_release=on_release)
    t1.start()




    def on_move(x, y):
        f.write('mouse|move|{0}\n'.format( (x, y)))
        print('mouse|move|{0}\n'.format( (x, y)))

    def on_click(x, y, button, pressed):
        f.write('{0}|{1}\n'.format( 'mouse press' if pressed else 'release', (x, y)))
        print('{0}|{1}\n'.format( 'mouse press' if pressed else 'release', (x, y)))

    def on_scroll(x, y, dx, dy):
        f.write('mouse|scroll|{0}|{1}\n'.format( 'down' if dy < 0 else 'up', (x, y)))
        print('mouse|scroll|{0}|{1}\n'.format( 'down' if dy < 0 else 'up', (x, y)))

    t2 = mouse.Listener( on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    t2.start()

    while t1.running:
        sleep(0.1)
        if not t1.running:
            t2.stop()


    f.close()
    print "closing"


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







