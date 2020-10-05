#!/usr/bin/python3

import ondotoridata
import ambient

ambi = ambient.Ambient(27153, "e26f5bd118ca9cb7")

login_id = 'tbac0004'
login_pass = 'bukkuden'
devices = ondotoridata.getCurrentDataFromWebStorage(login_id, login_pass)
for device in devices['devices']:
    if device['serial'] == '5214C18D':
        battery = device['battery']
        ambi.send({"d1": int(battery)})
