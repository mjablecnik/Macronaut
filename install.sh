#!/bin/bash


apt-get install xdotool

cp -r lib/* /usr/lib/python2.7/
cp -r src/{macro.py,config.py} /usr/lib/python2.7/
cp src/macronaut /usr/bin/macronaut


