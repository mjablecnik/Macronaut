#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Program for generating automatic scripts.
  
"""

import os, sys
from time import sleep, time
import ast
import config
from pynput import mouse, keyboard


def write_line(file, text):
    file.write( text )
    print( text.splitlines()[0] )


def record(raw_file):
    f = open(raw_file, 'w')
    f.close()
    f = open(raw_file, 'a')

    def on_press(key):
        write_line( f, 'keyboard|press|{0}\n'.format(key) )

    def on_release(key):
        write_line( f, 'keyboard|release|{0}\n'.format(key) )
        if key == keyboard.Key.esc:
            # Stop listener
            return False


    t1 = keyboard.Listener(on_press=on_press, on_release=on_release)
    t1.start()



    def on_move(x, y):
        write_line( f, 'mouse|move|{0}\n'.format( (x, y)))

    def on_click(x, y, button, pressed):
        write_line( f, 'mouse|{0}|{1}\n'.format( 'press' if pressed else 'release', (x, y)))

    def on_scroll(x, y, dx, dy):
        write_line( f, 'mouse|scroll-{0}|{1}\n'.format( 'down' if dy < 0 else 'up', (x, y)))

    t2 = mouse.Listener( on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    t2.start()

    while t1.running:
        sleep(0.1)
        if not t1.running:
            t2.stop()


    f.close()
    print "closing"



class SpecialKeys:
    ctrl = False
    alt = False
    shift = False

    @staticmethod
    def get_attributes():
        return SpecialKeys.__dict__
    @staticmethod
    def update_attributes(d):
        SpecialKeys.__dict__.update(d)
    @staticmethod
    def get_active_shortcut_keys():
        shortcut_keys = ""
        for key, value in SpecialKeys.__dict__.iteritems():
            if value == True:
                shortcut_keys += key + " + "
        return shortcut_keys


def compile_keyboard(f, data):
    def get_value_format(value):                                                  
        if value[0] == 'u':
            return SpecialKeys.get_active_shortcut_keys() + value[2:-1].replace('\\x','U')
        elif value[0:3] == 'Key':
            special_key = value.split('.')[1]
            keys_attrs = SpecialKeys.get_attributes()
            if special_key in keys_attrs.keys():
                keys_attrs[special_key] = True if data['event'] == 'press' else False
                SpecialKeys.update_attributes(keys_attrs)
            else:
                return special_key


    formated_value = get_value_format(unicode(data['value']))
    if data['event'] == 'press':
        if formated_value != None:
            write_line(f, 'xdotool keydown {0}\n'.format( formated_value ))

    elif data['event'] == 'release':
        if formated_value != None:
            write_line(f, 'xdotool keyup {0}\n'.format( formated_value ))


def compile_mouse(f, data):
    pass


# generating of macro code
def compile(raw_file, output_file):
    with open(raw_file,'r') as f: 
        lines = f.read().splitlines()

    f = open(output_file, 'w')
    f.close()
    f = open(output_file, 'a')


    for line in lines:
        data = line.split('|')
        data = dict(zip({ "input", "value", "event" }, data))

        if data['input'] == 'keyboard':
            compile_keyboard(f, data)
        elif data['input'] == 'mouse':
            compile_mouse(f, data)

    f.close()

    #text = ''
    #hotkey_str = ''
    #for event in events:
    #    if is_hotkey(event):
    #        hotkeys = event[1]
    #        hotkey_str = "xdotool key "
    #        for hotkey, value in hotkeys.items():
    #            if value:                                # if hotkey is pressed
    #                 hotkey_str += hotkey.split(' ')[1]  #add name of key
    #                 hotkey_str += "+"
    #        hotkey_str += "%s\n" % event[0]
    #        text += hotkey_str
    #    else:
    #        key = event[0]
    #        if key == '<enter>':
    #            text += "xdotool key Return\n"
    #        elif key == '<tab>':
    #            text += "xdotool key Tab\n"
    #        elif key == '<caps lock>':
    #            text += "xdotool key Escape\n"
    #        else:
    #            text += "xdotool key %s\n" % key 

    #file = open(file, 'w')
    #file.write(text)
    #file.close()







