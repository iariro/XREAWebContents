#!/usr/bin/python3

import cgi
import datetime
import ipmiutilcheck
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

try:
	versions = ipmiutilcheck.getIpmiutilVersion()
	print('Content-Type: text/html')
	print()
	print(
	'''<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta name="viewport" content="width=device-width">
	<title>ipmiutil version check</title>
	</head>
	<body>''')

	today = datetime.date.today()
	print('<table>')
	print('<tr><th>日付</th><th>開発者</th><th>バージョン</th><th>間隔</th></tr>')
	pd = None
	diff = None
	for version in versions[0:10]:
		diff_to_today = (today - version['date']).days
		if pd:
			diff = (pd - version['date']).days

		if diff:
			print('<tr><td>%s</td><td>%s</td><td>%s</td><td align="right">%s' % (version['date'], version['author'], version['version'], diff))
		else:
			print('<tr><td>%s</td><td>%s</td><td>%s</td><td align="right">%s' % (version['date'], version['author'], version['version'], diff_to_today))

		if diff_to_today < 30:
			print('<td><img src="http://sozai.akuseru-design.com/img_new/new025/new025_06.gif"></td>')

		print('</td></tr>')
		pd = version['date']
	print('</table>')
	print('</body></html>')
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
