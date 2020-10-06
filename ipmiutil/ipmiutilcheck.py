#!/usr/local/bin/python3
import datetime
import re
import urllib.request
from bottle import route, template
import ipmiutilchangelog

@route('/')
def index():
    try:
        return template('index.html', versions=ipmiutilchangelog.getIpmiutilVersion()[0:20])
    except Exception as e:
        return str(e)
