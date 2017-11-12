#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: File for transform keys from Pynput format into xdotool format.
  
"""


def transform(key):
    if key == 'esc': return 'Escape'
    elif key == 'alt': return 'Alt'
    elif key == 'alt_gr': return 'Alt_R'
    elif key == 'alt_l': return 'Alt_L'
    elif key == 'alt_r': return 'Alt_R'
    elif key == 'backspace': return 'BackSpace'
    elif key == 'caps_lock': return 'Caps_Lock'
    elif key == 'cmd': return 'Super'
    elif key == 'cmd_l': return 'Super_L'
    elif key == 'cmd_r': return 'Super_R'
    elif key == 'ctrl': return 'Control'
    elif key == 'ctrl_l': return 'Control_L'
    elif key == 'ctrl_r': return 'Control_R'
    elif key == 'delete': return 'Delete'
    elif key == 'down': return 'Down'
    elif key == 'end': return 'End'
    elif key == 'enter': return 'Return'
    elif key == 'f1': return 'F1'
    elif key == 'f2': return 'F2'
    elif key == 'f3': return 'F3'
    elif key == 'f4': return 'F4'
    elif key == 'f5': return 'F5'
    elif key == 'f6': return 'F6'
    elif key == 'f7': return 'F7'
    elif key == 'f8': return 'F8'
    elif key == 'f9': return 'F9'
    elif key == 'f10': return 'F10'
    elif key == 'f11': return 'F11'
    elif key == 'f12': return 'F12'
    elif key == 'home': return 'Home'
    elif key == 'insert': return 'Insert'
    elif key == 'left': return 'Left'
    elif key == 'menu': return 'Menu'
    elif key == 'num_lock': return 'Num_Lock'
    elif key == 'page_down': return 'Page_Down'
    elif key == 'page_up': return 'Page_Up'
    elif key == 'pause': return 'Pause'
    elif key == 'print_screen': return 'Print'
    elif key == 'right': return 'Right'
    elif key == 'scroll_lock': return 'Scroll_Lock'
    elif key == 'shift': return 'Shift'
    elif key == 'shift_l': return 'Shift_L'
    elif key == 'shift_r': return 'Shift_R'
    elif key == 'space': return 'space'
    elif key == 'tab': return 'Tab'
    elif key == 'up': return 'Up'
    else: return key
