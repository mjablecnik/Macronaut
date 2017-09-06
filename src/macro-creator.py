#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Script for record macros
  
"""


import getopt, sys, os, ast
import keylogger
from time import sleep, time
import argparse


# Constants
SCRIPT_PATH = os.path.dirname(sys.argv[0])

TMP_PATH = '/tmp/macro-creator'
STOP_FILE = TMP_PATH + '/stop-rec'   # if doesn't exist so recording is stopped
TMP_DIR = TMP_PATH + '/keyrec/' 

OUTPUT_PATH = SCRIPT_PATH + '/tmp/macro/'

RAW_FILE = TMP_DIR + 'macro-data'




# record macro
def record_macro(raw_file=RAW_FILE):
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



# load code from recorder file
def load_data():
    file = open(RAW_FILE, 'r')
    lines = file.readlines()
    file.close()
    return lines


# Parse code
def parse(lines):
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

# generating of code
def compile(events):
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
#    hotkey('ctrl', 'alt', 'h')

    


# save generated code
def save_macro(text, name='macro-output.py', macro_path=SCRIPT_PATH + '/tmp/macro/'):
    file = open(macro_path+'/'+name, 'w')

    head = """#!/usr/bin/env python

from pyautogui import hotkey, typewrite, click
from time import sleep
sleep(0.5)
"""
    file.write(head+text)
    file.close()



def prepare():
    os.system('mkdir -p ' + TMP_DIR)
    os.system("touch " + STOP_FILE)
    os.system('mkdir -p ' + OUTPUT_PATH)

    keystate = {
         'left ctrl': False,
         'left alt': False,
         'left shift': False,
         'right ctrl': False,
         'right alt': False,
         'right shift': False,
    }

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true', default=False, dest='record', help='Setup record')
    parser.add_argument('--compile', action='store_true', default=False, dest='compile', help='Setup compile')
    parser.add_argument('--name', action='store', default="macro_example", dest='name', help='Setup name')
    parser.add_argument('--output-path', action='store', default=OUTPUT_PATH, dest='output_path', help='Setup macro OUTPUT_PATH')
    return parser.parse_args()


def main():
    prepare()
    args = parse_arguments()
    #print args.record
    #print args.compile
    #print args.name
    #print args.output_path

    if args.record:
        record_macro()		
    if args.compile:
        parsed_data = parse(load_data())
        generated_code = compile(parsed_data)
        save_macro(generated_code, args.name, args.output_path)
    else:
        record_macro()		
        parsed_data = parse(load_data())
        generated_code = compile(parsed_data)
        save_macro(generated_code, args.name, args.output_path)



if __name__ == "__main__":
    main()
