#!/usr/bin/python3

import os
import sys
import io
from bottle import route, template
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import ipmiutilcheck

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

@route('/')
def index():
    try:
        return template('index.html', versions=ipmiutilcheck.getIpmiutilVersion()[0:10])
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    print(index())
