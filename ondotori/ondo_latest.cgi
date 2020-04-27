#!/usr/bin/python3

import cgi
import datetime
import json
import urllib.request
import ondotori
import sys, io

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
    form = cgi.FieldStorage()
    login_id = form['login_id'].value
    login_pass = form['login_pass'].value
    remote_serial = form['remote_serial'].value

    daily = ondotori.getLatestDataFromWebStorage(login_id, login_pass, remote_serial)
    data_hours = ondotori.getDaysSeries(daily)
    data_mean = ondotori.getMeanOfDaySeries(daily)
    data_max = ondotori.getMaxOfDaySeries(daily)
    data_min = ondotori.getMinOfDaySeries(daily)

    print('Content-Type: text/html')
    print()
    print(
    '''<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv=Content-Style-Type content=text/css>
    <link rel="stylesheet" type="text/css" href="hatena.css">
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://code.highcharts.com/highcharts.js"></script>
    <title>おんどとり - 短期グラフ</title>
    </head>

    <body>
    <div id="chart_days" style="width:900px; height:400px; display:table;margin: 0 auto;"></div>
    <div id="chart_mean" style="width:900px; height:600px; margin: 0 auto;"></div>
    <script type="text/javascript">
    function draw()
    {
        new Highcharts.Chart(
        {
            chart: {renderTo: 'chart_days', zoomType:'xy', plotBackgroundColor: 'lightgray'},
            title: {text: '日ごとの変動 直近５日分'},
            xAxis: {title: 'Hour', tickInterval:1},
            yAxis: {title: {text:'℃'}},
            series: [ %s ]
        });
        new Highcharts.Chart(
        {
            chart: {renderTo: 'chart_mean', zoomType:'xy', plotBackgroundColor: 'lightgray'},
            title: {text: '日ごとの平均・最高・最低気温'},
            xAxis: {title: 'Date', type: 'datetime'},
            yAxis: {title: {text:'℃'}},
            series: [ {name:'平均気温', type:'column', data:[%s]}, {name:'最高気温', type:'line', data:[%s]}, {name:'最低気温', type:'line', data:[%s]} ]
        });
    };
    document.body.onload = draw();
    </script>
    <br>
    </body>
    </html>''' % (data_hours, data_mean, data_max, data_min))

except Exception as e:
    print('Content-Type: text/html')
    print()
    print(
    '''<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html">
    </head>
    <body>
    <pre>%s</pre>
    </body></html>''' % e)
