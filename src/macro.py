#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2018 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Program for generating automatic scripts.
  
"""

import os, sys
from time import sleep, time
import config, keys
from pynput import mouse, keyboard



def write_line(file, text):
    file.write( text )
    if (config.VERBOSE):
        print( text.splitlines()[0] )


def record(path, name):
    full_file_path = os.path.join(path, name+".raw")
    open(full_file_path, 'w').close() # clear file
    f = open(full_file_path, 'a')
    start_time = time()


    #####    Keyboard thread   #####
    def on_press(key):
        write_line(f, 'keyboard|press|{0}|{1}\n'.format( key, round(time() - start_time, 4) ))

    def on_release(key):
        write_line(f, 'keyboard|release|{0}|{1}\n'.format( key, round(time() - start_time, 4) ))
        if key == keyboard.Key.ctrl_r:
            return False


    keyboard_thread = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_thread.start()



    #####    Mouse thread   #####
    def on_move(x, y):
        write_line( f, 'mouse|move|{0}|{1}\n'.format( (x, y), round(time() - start_time, 4) ))

    def on_click(x, y, button, pressed):
        write_line( f, 'mouse|{0}|{1}|{2}\n'.format( 'press' if pressed else 'release', button, round(time() - start_time, 4) ))

    def on_scroll(x, y, dx, dy):
        write_line( f, 'mouse|scroll-{0}|{1}|{2}\n'.format( 'down' if dy < 0 else 'up', (x, y), round(time() - start_time, 4) ))

    mouse_thread = mouse.Listener( on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_thread.start()



    #####    Main thread loop   #####
    while keyboard_thread.running:
        sleep(0.1)
        if not keyboard_thread.running:
            mouse_thread.stop()


    f.close()
    print "Recorded data was saved into: " + path





##  Compile macro code  
def compile_keyboard(f, data):
    def transform_value(value):                                                  
        if value[0] == 'u':
            return keys.transform(value[2:-1].replace('\\x','U'))

        elif value[0:3] == 'Key':
            special_key = value.split('.')[1]
            return keys.transform(special_key)


    transformed_value = transform_value(unicode(data['value']))
    if data['event'] == 'press':
        if transformed_value != None:
            write_line(f, 'xdotool keydown {0}\n'.format( transformed_value ))

    elif data['event'] == 'release':
        if transformed_value != None:
            write_line(f, 'xdotool keyup {0}\n'.format( transformed_value ))


def compile_mouse(f, data):
    def transform_value(value):
        if value == "Button.left":
            return 1
        elif value == "Button.middle":
            return 2
        elif value == "Button.right":
            return 3

    transformed_value = transform_value(data['value'])
    if data['event'] == 'press':    
        if transformed_value != None:
            write_line(f, 'xdotool mousedown {0}\n'.format( transformed_value ))
    elif data['event'] == 'release':
        if transformed_value != None:
            write_line(f, 'xdotool mouseup {0}\n'.format( transformed_value ))
    elif data['event'] == 'move':
        x, y = eval(data['value'])
        write_line(f, 'xdotool mousemove {0} {1}\n'.format( x, y ))
    elif data['event'] == 'scroll-down':
        write_line(f, 'xdotool click 5\n')
    elif data['event'] == 'scroll-up':
        write_line(f, 'xdotool click 4\n')
        


## Generate macro code
def compile(raw_path, output_path, name, speed):
    full_raw_path = os.path.join(raw_path, name+".raw")
    full_output_path = os.path.join(output_path, name+".macro")

    # read raw file
    with open(full_raw_path,'r') as f: 
        lines = f.read().splitlines()

    # clean old macro
    open(full_output_path, 'w').close()

    # write new macro
    f = open(full_output_path, 'a')
    previous_time = 0.0

    for i in range(len(lines)):
        data = lines[i].split('|')
        data = dict(zip({ "input", "value", "event", "time" }, data))

        write_line(f, "sleep {0}\n".format( ( float(data['time']) - previous_time) / speed ))

        if data['input'] == 'keyboard':
            compile_keyboard(f, data)
        elif data['input'] == 'mouse':
            compile_mouse(f, data)

        previous_time = float(data['time'])

    f.close()



