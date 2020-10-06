#!/usr/bin/python3
import ipmiutilchangelog
import ambient
import requests

def line_notify(last, now):
    token = "nPQEoC190nfvydJRbQmY75SY00Ygvt0CxsaXWoLTUUH"
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": 'ipmiutilのバージョンがv%sからv%sになりました' % (last, now)}
    requests.post(url, headers=headers, data=payload)

if __name__ == '__main__':
    amb = ambient.Ambient(27186, 'd2ec99843c2a366c', 'c7224d23ad8524cd')
    last = amb.read(n=1)
    if len(last) > 0:
        last = len[0]['d1']
    else:
        last = None
    now = ipmiutilchangelog.getIpmiutilVersion()[0]['version']
    now = int(now.replace('.', ''))
    amb.send({'d1': now})

    if now != last:
        line_notify(last, now)
