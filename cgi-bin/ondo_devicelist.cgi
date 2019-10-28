#!/usr/bin/python3

import cgi
import ondotori
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

try:
	form = cgi.FieldStorage()
	login_id = form['login_id'].value
	login_pass = form['login_pass'].value
	devices = ondotori.getCurrentDataFromWebStorage(login_id, login_pass)
	image_url = 'https://ondotori.webstorage.jp/img/device/tr7.svg'

	print('Content-Type: text/html')
	print()
	print(
	'''<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	</head>
	<body>''')

	print('<table border><tr><th>モデル</th><th>シリアルNo</th><th>電池残量</th>')
	print('<th>取得日時</th><th>温度</th><th>湿度</th><th>グラフ</th></tr>')
	for device in devices['devices']:
		print('<tr><td><img src="%s"><br>%s</td><td>%s</td><td align="right">%s</td>' %
			(image_url,
			device['model'],
			device['serial'],
			device['battery']))
		print('<td align="right">%s</td><td align="right">%s %s</td><td align="right">%s %s</td>' %
			(device['datetime'],
			device['channel'][0]['value'],
			device['channel'][0]['unit'],
			device['channel'][1]['value'],
			device['channel'][1]['unit']))

		print('''<td><form action="ondo_latest.cgi" method="post">
			<input type="hidden" name="login_id" value="%s" />
			<input type="hidden" name="login_pass" value="%s" />
			<input type="hidden" name="remote_serial" value="%s" />
			<input type="submit" value="短期グラフ" /></form>''' % (login_id, login_pass, device['serial']))
		print('''<form action="ondo_all.cgi" method="post">
			<input type="hidden" name="login_id" value="%s" />
			<input type="hidden" name="login_pass" value="%s" />
			<input type="hidden" name="remote_serial" value="%s" />
			<input type="submit" value="長期グラフ" /></form></td>''' % (login_id, login_pass, device['serial']))
		print('</tr>')
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
