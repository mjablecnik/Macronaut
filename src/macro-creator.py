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


# Constants
SCRIPT_PATH = os.path.dirname(sys.argv[0])

TMP_PATH = '/tmp/macro-creator'
STOP_FILE = TMP_PATH + '/stop-rec'   # if doesn't exist so recording is stopped
TMP_DIR = TMP_PATH + '/keyrec/' 

MACRO_DIR = SCRIPT_PATH + '/tmp/macro/'

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
    os.system('mkdir -p ' + MACRO_DIR)

    keystate = {
         'left ctrl': False,
         'left alt': False,
         'left shift': False,
         'right ctrl': False,
         'right alt': False,
         'right shift': False,
    }

def help():
    print("\n\nYou need run program with this parameters:")
    print("--record      -- for record macro")
    print("--compile     -- for complie macro")
    print("--name        -- for record, compile and save macro under specific name")
    print("\n\n")

def main():
    prepare()
    if len(sys.argv) > 1:
	if sys.argv[1] == "--record":
            record_macro()		
	elif sys.argv[1] == "--compile":
            parsed_data = parse(load_data())
            generated_code = compile(parsed_data)
            save_macro(generated_code)
	elif sys.argv[1] == "--name":
            if len(sys.argv) > 2:
                if sys.argv[3] == "--output-path":
                    macro_path = sys.argv[4]

                macro_name = sys.argv[2]
                record_macro()		
                parsed_data = parse(load_data())
                generated_code = compile(parsed_data)
                save_macro(generated_code, macro_name, macro_path)
            else:
                print("You need type name!!")
                print("For example:  'python macro-creator.py --name \"macro_name_example\"'")
	elif sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
            help()
    else:
        help()
    


if __name__ == "__main__":
    main()
