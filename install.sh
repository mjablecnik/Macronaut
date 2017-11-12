#!/bin/bash
set -e

pip install pynput==1.3.7 
apt-get install xdotool

echo src/config.py | xargs perl -pi -E "s/DEVEL=True/DEVEL=False/g"

cp -r src/*.py /usr/lib/python2.7/
cp src/macronaut /usr/bin/macronaut


