#!/usr/bin/python3

import os
import sys
import io
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import ipmiutilcheck  # noqa F401

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
