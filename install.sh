#!/bin/bash
set -e

pip install pynput==1.3.7 docopt==0.6.2
apt-get install xdotool zenity

sed -i -e 's/DEVEL=True/DEVEL=False/g' src/config.py

mkdir -p /usr/lib/python2.7/macronaut/
cp -r src/*.py /usr/lib/python2.7/macronaut/
cp src/macronaut /usr/bin/macronaut


