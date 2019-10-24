#!/usr/bin/python3

import ondotori
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

devices = ondotori.getCurrentDataFromWebStorage()
image_url = 'https://ondotori.webstorage.jp/img/device/tr7.svg'

print('Content-Type: text/html')
print()
print(
'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>''')

print('<table border><tr><th>モデル</th><th>シリアルNo</th><th>電池残量</th><th>取得日時</th><th>温度</th><th>湿度</th></tr>')
for device in devices['devices']:
	print('<tr><td><img src="%s"><br>%s</td><td>%s</td><td align="right">%s</td><td align="right">%s</td><td align="right">%s %s</td><td align="right">%s %s</td></tr>' %
		(image_url,
		device['model'],
		device['serial'],
		device['battery'],
		device['datetime'],
		device['channel'][0]['value'],
		device['channel'][0]['unit'],
		device['channel'][1]['value'],
		device['channel'][1]['unit']))
print('</table>')
print('</body></html>')
