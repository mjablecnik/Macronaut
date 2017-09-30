#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pynput import keyboard

def on_press(key):
    try:
        print(u'alphanumeric key {0} pressed'.format(unicode(key.char)))
    except AttributeError:
        print(u'special key {0} pressed'.format(unicode(key)))

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    try:
        print(u'key {0} released'.format(key.char))
    except AttributeError:
        print(u'special key {0} released'.format(unicode(key)))


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

