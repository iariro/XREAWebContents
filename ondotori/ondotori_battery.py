#!/usr/bin/python3

import ondotoridata
import ambient
import requests

def get_battery():
    login_id = 'tbac0004'
    login_pass = 'bukkuden'
    devices = ondotoridata.getCurrentDataFromWebStorage(login_id, login_pass)
    for device in devices['devices']:
        if device['serial'] == '5214C18D':
            return int(device['battery'])

def line_notify(last, now):
    token = "nPQEoC190nfvydJRbQmY75SY00Ygvt0CxsaXWoLTUUH"
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": 'おんどとりの電池残量が%dから%dになりました' % (last, now)}
    requests.post(url, headers=headers, data=payload)

if __name__ == '__main__':
    amb = ambient.Ambient(27153, 'e26f5bd118ca9cb7', '5ec1d2977853fa8c')
    last = amb.read(n=1)[0]['d1']
    now = get_battery()
    amb.send({'d1': now})

    if now != last:
        line_notify(last, now)
