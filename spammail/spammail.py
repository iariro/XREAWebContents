#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, template, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import smammaildata

@route('/')
def index():
    return template('index.html')

@route('/input')
def input():
    return template('input.html', date=datetime.datetime.now().strftime('%Y/%m/%d'))

@route('/input2', method="POST")
def input2():
    try:
        date = request.POST.getunicode('date')
        sm_count = request.POST.getunicode('sm_count')
        smammaildata.add(date, sm_count)
        return template('input2.html', date=date, sm_count=sm_count)
    except Exception as e:
        return str(e)

@route('/graph')
def graph():
    try:
        daily_num = smammaildata.read_data()
        return template('graph.html',
                        daily_num_x=[day.strftime('%Y/%m/%d') for day in daily_num],
                        daily_num_y=list(daily_num.values()))
    except Exception as e:
        return str(e)
