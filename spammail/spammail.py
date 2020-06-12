#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, template, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import spammaildata

@route('/')
def index():
    return template('index.html')

@route('/input')
def input():
    date = datetime.datetime.now()
    date -= datetime.timedelta(days=1)
    return template('input.html', date=date.strftime('%Y/%m/%d'))

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
        daily_num = spammaildata.read_data()
        return template('graph.html',
                        daily_num=[[day.timestamp() * 1000, count] for day, count in daily_num.items()])
    except Exception as e:
        return str(e)
