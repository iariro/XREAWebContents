# coding: utf-8
#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, run, template, static_file, get, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import coronadata

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
		infect_num = request.POST.getunicode('infect_num')
		coronadata.add(date, infect_num)
		return template('input2.html', date=date, infect_num=infect_num)
	except Exception as e:
		return str(e)

@route('/graph')
def graph():
	try:
		daily_num = coronadata.read_data()
		weeks, weekly_num = coronadata.statistic_weekly(daily_num, '2020/03/02', '2020/04/19')
		return template('graph.html',
			daily_num_x=[day.strftime('%Y/%m/%d') for day in daily_num],
			daily_num_y=list(daily_num.values()),
			weekly_num_x=weeks,
			weekly_num_y=[{'name': day.strftime('%Y/%m/%d'), 'data': values} for day, values in weekly_num.items()],
			weekly_num=weekly_num)
	except Exception as e:
		return str(e)
