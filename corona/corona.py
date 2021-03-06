#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, template, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import coronadata

@route('/')
def index():
    try:
        daily_num = coronadata.read_last_data(5)
        return template('index.html', daily_num=daily_num)
    except Exception as e:
        return str(e)

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

@route('/update')
def update():
    date = datetime.datetime.now() + datetime.timedelta(days=-2)
    return template('update.html', date=date.strftime('%Y/%m/%d'))

@route('/update2', method="POST")
def update2():
    try:
        date = request.POST.getunicode('date')
        infect_num = request.POST.getunicode('infect_num')
        coronadata.update(date, infect_num)
        return template('input2.html', date=date, infect_num=infect_num)
    except Exception as e:
        return str(e)

@route('/graph')
def graph():
    jpweek = {'Mon': '月曜', 'Tue': '火曜', 'Wed': '水曜',
              'Thu': '木曜', 'Fri': '金曜', 'Sat': '土曜', 'Sun': '日曜'}
    try:
        end_date = coronadata.last_complete_week_start(datetime.datetime.today())
        daily_num = coronadata.read_mhlw_data()
        weeks, weekly_num = coronadata.statistic_weekly(daily_num,
                                                        datetime.datetime(2020, 3, 2),
                                                        end_date)
        weekday_date, weekday_num = coronadata.statistic_weekday(daily_num,
                                                                 datetime.datetime(2020, 3, 2),
                                                                 datetime.datetime.today())
        weekday_num = [{'name': jpweek[weekday], 'data': nums}
                       for weekday, nums in weekday_num.items()]
        weekly_sum = coronadata.sum_weekly(daily_num)
        weekly_num_y = [{'name': day.strftime('%Y/%m/%d'), 'data': values}
                        for day, values in weekly_num.items()]
        return template('graph.html',
                        daily_num_x=[day.strftime('%Y/%m/%d') for day in daily_num],
                        daily_num_y=list(daily_num.values()),
                        weekly_sum_x=[day.strftime('%Y/%m/%d') for day in weekly_sum.keys()],
                        weekly_sum_y=list(weekly_sum.values()),
                        weekly_num_x=weeks,
                        weekly_num_y=weekly_num_y,
                        weekly_num=weekly_num,
                        weekday_date=weekday_date,
                        weekday_num=weekday_num)
    except Exception as e:
        return str(e)
