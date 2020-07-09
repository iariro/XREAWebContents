#!/usr/bin/python3

import cgi
import datetime
import json
import urllib.request
import ondotori
import sys, io
from statistics import mean

try:
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')
	form = cgi.FieldStorage()
	login_id = form['login_id'].value
	login_pass = form['login_pass'].value
	remote_serial = form['remote_serial'].value

	(monthly, weekly, daily) = ondotori.getAllDataFromWebStorage(login_id, login_pass, remote_serial)

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
	<title>おんどとり - 長期グラフ</title>
	</head>

	<body>
	<div id="chart_weekly" style="width:900px; height:400px; display:table;margin: 0 auto;"></div>
	<div id="chart_monthly" style="width:900px; height:400px; display:table;margin: 0 auto;"></div>
	<div id="chart_year" style="width:900px; height:500px; display:table;margin: 0 auto;"></div>
	<script type="text/javascript">
	function draw()
	{
	        new Highcharts.Chart(
	        {
	                chart: {renderTo: 'chart_weekly', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
	                title: {text: '週ごと平均'},
	                xAxis: {title: '日', type: 'datetime'},
	                yAxis: {title: {text:'℃'}},
	                series: [ {name:'温度', data:[%s]} ]
	        });
	        new Highcharts.Chart(
	        {
	                chart: {renderTo: 'chart_monthly', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
	                title: {text: '月ごと平均'},
	                xAxis: {title: '日', type: 'datetime'},
	                yAxis: {title: {text:'℃'}},
	                series: [ {name:'温度', data:[%s]} ]
	        });
	        new Highcharts.Chart(
	        {
	                chart: {renderTo: 'chart_year', zoomType:'xy', plotBackgroundColor: 'lightgray'},
	                title: {text: '年毎比較'},
	                xAxis: {title: '日', type: 'datetime'},
	                yAxis: {title: {text:'℃'}},
	                series: %s
	        });
	};
	document.body.onload = draw();
	</script>
	<br>
	</body>
	</html>''' % (ondotori.getMeanOfDaySeries(weekly),
                  ondotori.getMeanOfDaySeries(monthly),
                  ondotori.getMeanOfDaySeriesPerYear(daily, 9)))
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
