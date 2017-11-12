#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Program for generating automatic scripts.
  
"""

import os, sys
from time import sleep, time
import config, keys
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



def compile_keyboard(f, data):
    
    def get_value_format(value):                                                  
        if value[0] == 'u':
            return keys.transform(value[2:-1].replace('\\x','U'))

        elif value[0:3] == 'Key':
            special_key = value.split('.')[1]
            return keys.transform(special_key)


    formated_value = get_value_format(unicode(data['value']))
    if data['event'] == 'press':
        if formated_value != None:
            write_line(f, 'xdotool keydown {0}\n'.format( formated_value ))

    elif data['event'] == 'release':
        if formated_value != None:
            write_line(f, 'xdotool keyup {0}\n'.format( formated_value ))
            #write_line(f, 'sleep 0.1\n')


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



