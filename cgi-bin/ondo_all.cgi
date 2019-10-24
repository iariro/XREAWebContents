#!/usr/bin/python3

import datetime
import json
import urllib.request
import ondotori

(monthly, weekly) = ondotori.getAllDataFromWebStorage()

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
<div id="chart_weekly" style="width:900px; height:400px; display:table;margin: 0 auto;"></div>
<div id="chart_monthly" style="width:900px; height:400px; display:table;margin: 0 auto;"></div>
<script type="text/javascript">
function draw()
{
        new Highcharts.Chart(
        {
                chart: {renderTo: 'chart_weekly', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
                title: {text: 'Weekly'},
                xAxis: {title: 'Date', type: 'datetime'},
                yAxis: {title: {text:'degrees C'}},
                series: [ {name:'Mean temp', data:[%s]} ]
        });
        new Highcharts.Chart(
        {
                chart: {renderTo: 'chart_monthly', type:'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
                title: {text: 'Monthly'},
                xAxis: {title: 'Date', type: 'datetime'},
                yAxis: {title: {text:'degrees C'}},
                series: [ {name:'Mean temp', data:[%s]} ]
        });
};
document.body.onload = draw();
</script>
<br>
</body>
</html>''' % (ondotori.getMeanOfDaySeries(weekly), ondotori.getMeanOfDaySeries(monthly)))
