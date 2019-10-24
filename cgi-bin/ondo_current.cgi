#!/usr/bin/python3

import ondotori

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

print('<table border><tr><th>Model</th><th>Serial</th><th>Battery</th><th>Temp</th><th>Humid</th></tr>')
for device in devices['devices']:
	print('<tr><td><img src="%s"><br>%s</td><td>%s</td><td align="right">%s</td><td align="right">%s %s</td><td align="right">%s %s</td></tr>' %
		(image_url,
		device['model'],
		device['serial'],
		device['battery'],
		device['channel'][0]['value'],
		device['channel'][0]['unit'],
		device['channel'][1]['value'],
		device['channel'][1]['unit']))
print('</table>')
print('</body></html>')
