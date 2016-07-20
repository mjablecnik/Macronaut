#!/usr/bin/env python
import getopt, sys, os

from pyautogui import hotkey, typewrite, click
import ast

import keylogger
from time import sleep, time


STOP_FILE = '/home/martin/tmp/stop-rec'   # if dont exist so recording is stopped

TMP_DIR = '/home/martin/tmp/keyrec/' 
RAW_FILE = TMP_DIR + 'macro-data'


MACRO_DIR = '/home/martin/macro/'
MACRO_NAME = 'autocmd.py'

os.system("touch %s && mkdir %s" % (STOP_FILE, TMP_DIR))
os.system('mkdir ' + MACRO_DIR)

keystate = {
     'left ctrl': False,
     'left alt': False,
     'left shift': False,
     'right ctrl': False,
     'right alt': False,
     'right shift': False,
 }



# RECORD MACRO
def record_macro(raw_file=RAW_FILE):
    file = open(raw_file, 'w')
    def print_keys(t, modifiers, keys): 
        text_format = ("%.2f|%r|%r\n" % (t, keys, modifiers))
        file.write(text_format)
        print(text_format)


    while os.path.isfile(STOP_FILE):
        sleep(.005)
        changed, modifiers, keys = keylogger.fetch_keys()
        if changed: 
            print_keys(time(), modifiers, keys)

    file.close()



# LOAD CODE FROM RECORDER FILE
def load_data():
    file = open(RAW_FILE, 'r')
    lines = file.readlines()
    file.close()
    return lines


# PARSE CODE
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



# Check if hotkey is pressed
def is_hotkey(event):
    hotkeys = event[1]
    for hotkey, value in hotkeys.items():
        if value:                                # if hotkey is pressed
            return True
    return False

# GENERATING OF CODE
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

    


# SAVE GENERATED CODE
def save_macro(text):
    file = open(MACRO_DIR+MACRO_NAME, 'w')

    head = """#!/usr/bin/env python

from pyautogui import hotkey, typewrite, click
from time import sleep
sleep(0.5)
"""
    file.write(head+text)
    file.close()




def main():
    if len(sys.argv) > 1:
	if sys.argv[1] == "rec" or sys.argv[1] == "record":
            record_macro()		
	elif sys.argv[1] == "comp" or sys.argv[1] == "compile":
            parsed_data = parse(load_data())
            generated_code = compile(parsed_data)
            save_macro(generated_code)
        else:
            MACRO_NAME = sys.argv[1]
            record_macro()		
            parsed_data = parse(load_data())
            generated_code = compile(parsed_data)
            save_macro(generated_code)
    


if __name__ == "__main__":
    main()
