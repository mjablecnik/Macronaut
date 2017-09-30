#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Script for record macros
  
"""


import sys, os
import argparse
import macro, config


def prepare():
    os.system("touch " + config.STOP_FILE)
    os.system('mkdir -p ' + config.OUTPUT_PATH)

def clear():
    os.system("rm -rf " + config.RAW_FILE)
    os.system("rm -rf " + config.STOP_FILE)

    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true', default=False, dest='record', help='Only record keyboard inputs and save into raw_data format.')
    parser.add_argument('--compile', action='store_true', default=False, dest='compile', help='Compile raw_data format into python runable script which is saved into OUTPUT_PATH.')
    parser.add_argument('--play', action='store_true', default=False, dest='play', help='Play macro script.')
    parser.add_argument('-d', action='store_true', default=False, dest='debug', help='Run program in debug mode.')
    parser.add_argument('--name', action='store', default="macro_example", dest='name', help='Change name of macro script.')
    parser.add_argument('--output-path', action='store', default=config.OUTPUT_PATH, dest='output_path', help='Setup path where save generated macro script.')
    return parser.parse_args()



def main():
    prepare()
    args = parse_arguments()
    print config.RAW_FILE

    if args.record:
        macro.record(config.RAW_FILE)		
    if args.compile:
        with open(config.RAW_FILE,'r') as f: 
            macro.compile(f.readlines(), args.output_path+'/'+args.name)
    if args.play:
        os.system('bash '+args.output_path+'/'+args.name)
    #if not args.debug: clear()



if __name__ == "__main__":
    main()
