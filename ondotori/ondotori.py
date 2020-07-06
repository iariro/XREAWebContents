import datetime
import json
import urllib.request
from statistics import mean
import unittest

apikey = "j8j04n070kccokm8c7odoa89m6tjbi0qt69o4k8dac1n1"

def getCurrentDataFromWebStorage(login_id, login_pass):
    url = 'https://api.webstorage.jp/v1/devices/current'
    headers = {
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }
    req_data = {"api-key": apikey, "login-id": login_id, "login-pass": login_pass}
    req = urllib.request.Request(url, json.dumps(req_data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        devices = json.loads(body.decode())
        for device in devices['devices']:
            device['datetime'] = datetime.datetime.fromtimestamp(int(device['unixtime']))
    return devices

def getAllDataFromWebStorage(login_id, login_pass, remote_serial):
    url = 'https://api.webstorage.jp/v1/devices/data'
    headers = {
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }
    req_data = {"api-key": apikey,
                "login-id": login_id,
                "login-pass": login_pass,
                "remote-serial": remote_serial}

    monthly = {}
    weekly = {}
    req = urllib.request.Request(url, json.dumps(req_data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        js = json.loads(body.decode())
        for row in js['data']:
            dt = datetime.datetime.fromtimestamp(int(row['unixtime']))
            temp = float(row['ch1'])

            week = (dt - datetime.timedelta(days=dt.weekday())).strftime('%Y/%m/%d')
            if week not in weekly:
                weekly[week] = []
            weekly[week].append(temp)

            month = datetime.date(dt.year, dt.month, 1).strftime('%Y/%m/%d')
            if month not in monthly:
                monthly[month] = []
            monthly[month].append(temp)
    return (monthly, weekly)

def getLatestDataFromWebStorage(login_id, login_pass, remote_serial):
    url = 'https://api.webstorage.jp/v1/devices/latest-data'
    headers = {
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }
    req_data = {"api-key": apikey,
                "login-id": login_id,
                "login-pass": login_pass,
                "remote-serial": remote_serial}

    daily = {}
    req = urllib.request.Request(url, json.dumps(req_data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        js = json.loads(body.decode())
        for row in js['data']:
            dt = datetime.datetime.fromtimestamp(int(row['unixtime']))
            date = dt.strftime('%Y/%m/%d')
            if date not in daily:
                daily[date] = [None] * 24
            temp = float(row['ch1'])
            daily[date][dt.hour] = temp
    return daily

def getDaysSeries(days):
    return ','.join(["{name:'%s', data:%s}" % (date[5:], [temp for temp in temps if temp])
                    for date, temps in sorted(days.items())[-5:]])

def getMeanOfDaySeries(days):
    return ','.join(["[%d, %.2f]" % (datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000, mean([temp for temp in temps if temp])) for date, temps in sorted(days.items())])

def getMaxOfDaySeries(days):
    return ','.join(["[%d, %.2f]" % (datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000, max([temp for temp in temps if temp])) for date, temps in sorted(days.items())])

def getMinOfDaySeries(days):
    return ','.join(["[%d, %.2f]" % (datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000, min([temp for temp in temps if temp])) for date, temps in sorted(days.items())])

class TestOndotoriData(unittest.TestCase):
    def test_getCurrentDataFromWebStorage(self):
        print(getCurrentDataFromWebStorage('tbac0004', 'bukkuden'))

    def test_getAllDataFromWebStorage(self):
        (monthly, weekly) = getAllDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        # print(monthly, weekly)
        with open('weekly.json', 'w') as file:
            json.dump(weekly, file)
        # print(getMaxOfDaySeries(json.load(open('weekly.json'))))
        print(monthly)

    def test_getLatestDataFromWebStorage(self):
        daily = getLatestDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        with open('daily.json', 'w') as file:
            json.dump(daily, file)
        # print(getDaysSeries(json.load(open('daily.json'))))

if __name__ == '__main__':
    unittest.main()
