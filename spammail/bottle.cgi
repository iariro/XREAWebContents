#!/usr/local/bin/python3
import os
import sys
from bottle import run, static_file, get
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import spammail
