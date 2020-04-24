#!/usr/local/bin/python3
import os
import sys
from bottle import route, run, template, static_file, get
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import corona

@get('/static/css/<filename:re:.*\.css>')
def css(filename):
    return static_file(filename, root="views")

if __name__=='__main__':
    DEBUG = os.path.exists(os.path.expanduser('~/debug'))
    if DEBUG:
        run(host='localhost', port=8080, debug=True)
    else:
        run(host='0.0.0.0', port=80, server="cgi")
