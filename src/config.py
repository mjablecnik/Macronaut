#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

  Copyright (c) 2016-2017 Martin Jablecnik
  Authors: Martin Jablecnik
  Description: Config file
  
"""
import os, sys

# Constants
SCRIPT_PATH = os.path.dirname(sys.argv[0])
OUTPUT_PATH = SCRIPT_PATH + '/tmp/macro'
RAW_FILE = OUTPUT_PATH + '/macro-raw-data'
STOP_FILE = OUTPUT_PATH + '/stop-rec'   # if doesn't exist so recording is stopped
