#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Script for record macros
  
"""


import sys, os
import argparse
import macro


# Constants
SCRIPT_PATH = os.path.dirname(sys.argv[0])

TMP_PATH = '/tmp/macro-creator'
TMP_DIR = TMP_PATH + '/keyrec/' 
STOP_FILE = TMP_PATH + '/stop-rec'   # if doesn't exist so recording is stopped

OUTPUT_PATH = SCRIPT_PATH + '/tmp/macro/'

RAW_FILE = TMP_DIR + 'macro-data'


def prepare():
    os.system('mkdir -p ' + TMP_DIR)
    os.system("touch " + STOP_FILE)
    os.system('mkdir -p ' + OUTPUT_PATH)

    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true', default=False, dest='record', help='Only record keyboard inputs and save into raw_data format.')
    parser.add_argument('--compile', action='store_true', default=False, dest='compile', help='Compile raw_data format into python runable script which is saved into OUTPUT_PATH.')
    parser.add_argument('--start', action='store_true', default=False, dest='start', help='Play macro script.')
    parser.add_argument('--name', action='store', default="macro_example", dest='name', help='Change name of macro script.')
    parser.add_argument('--output-path', action='store', default=OUTPUT_PATH, dest='output_path', help='Setup path where save generated macro script.')
    return parser.parse_args()


def main():
    prepare()
    args = parse_arguments()
    #print args.record
    #print args.compile
    #print args.name
    #print args.output_path

    if args.record:
        macro.record(RAW_FILE)		
    if args.compile:
        file = open(RAW_FILE, 'r')
        raw_data = file.readlines()
        generated_code = macro.compile(raw_data)
        macro.save(generated_code, args.name, args.output_path)
        file.close()
    if args.start:
        os.system('python '+args.output_path+'/'+args.name+' > /dev/null')



if __name__ == "__main__":
    main()
