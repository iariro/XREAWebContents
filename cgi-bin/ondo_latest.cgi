#!/usr/bin/python3

import datetime
import json
import urllib.request
import ondotori

daily = ondotori.getLatestDataFromWebStorage()

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
</head>

<body>
<div id="chart_days" style="width:900px; height:400px; text-align:center;"></div>
<div id="chart_mean" style="width:900px; height:400px; text-align:center;"></div>
<div id="chart_max" style="width:900px; height:400px; text-align:center;"></div>
<script type="text/javascript">
function draw()
{
        new Highcharts.Chart(
        {
                chart: {renderTo: 'chart_days', zoomType:'xy', plotBackgroundColor: 'lightgray'},
                title: {text: 'latest 5days'},
                xAxis: {title: 'Hour'},
                yAxis: {title: {text:'degrees C'}},
                series: [ %s ]
        });
        new Highcharts.Chart(
        {
                chart: {renderTo: 'chart_mean', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
                title: {text: 'mean temp'},
                xAxis: {title: 'Date', type: 'datetime'},
                yAxis: {title: {text:'degrees C'}},
                series: [ {name:'Mean temp', data:[%s]} ]
        });
        new Highcharts.Chart(
        {
                chart: {renderTo: 'chart_max', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
                title: {text: 'max temp'},
                xAxis: {title: 'Date', type: 'datetime'},
                yAxis: {title: {text:'degrees C'}},
                series: [ {name:'Max temp', data:[%s]} ]
        });
};
document.body.onload = draw();
</script>
<br>
</body>
</html>''' % (ondotori.getDaysSeries(daily), ondotori.getMeanOfDaySeries(daily), ondotori.getMaxOfDaySeries(daily)))
