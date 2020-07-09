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
    daily = {}
    req = urllib.request.Request(url, json.dumps(req_data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        js = json.loads(body.decode())
        for row in js['data']:
            dt = datetime.datetime.fromtimestamp(int(row['unixtime']))
            temp = float(row['ch1'])

            day = dt.date().strftime('%Y/%m/%d')
            if day not in daily:
                daily[day] = []
            daily[day].append(temp)

            week = (dt - datetime.timedelta(days=dt.weekday())).strftime('%Y/%m/%d')
            if week not in weekly:
                weekly[week] = []
            weekly[week].append(temp)

            month = datetime.date(dt.year, dt.month, 1).strftime('%Y/%m/%d')
            if month not in monthly:
                monthly[month] = []
            monthly[month].append(temp)
    return (monthly, weekly, daily)

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

def getMeanOfDaySeriesPerYear(daily, mean_range):
    ''' 年ごとの推移を取得。推移は移動平均する。

        Args:
            daily: { date: [temp] }
            mean_range: 移動平均する日数

        Returns:
            { 'name': year, 'data': [[datetime, temp]] }
    '''
    # 平均気温
    for day in daily:
        daily[day] = mean(daily[day])

    # 移動平均
    mean_range_center = mean_range // 2
    buff = []
    for day, values in daily.items():
        while len(buff) >= mean_range:
            del buff[0]
        buff.append((day, values))
        if len(buff) == mean_range:
            daily[buff[mean_range_center][0]] = round(mean([value for day, value in buff]), 3)

    # 年ごとにまとめる
    years = {}
    for day, value in daily.items():
        if day[:4] not in years:
            years[day[:4]] = {}
        years[day[:4]][day[5:]] = value
    series = []
    for year in years:
        series.append({'name': year,
                       'data': [[datetime.datetime.strptime('2020/' + date, '%Y/%m/%d').timestamp() * 1000, value] for date, value in years[year].items()]})
    return series

####################################################################################################

class TestOndotoriData(unittest.TestCase):
    def test_getCurrentDataFromWebStorage(self):
        # print(getCurrentDataFromWebStorage('tbac0004', 'bukkuden'))
        pass

    def test_getAllDataFromWebStorage_dump(self):
        (monthly, weekly, daily) = getAllDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        with open('monthly.json', 'w') as file:
            json.dump(monthly, file)
        with open('weekly.json', 'w') as file:
            json.dump(weekly, file)
        with open('daily.json', 'w') as file:
            json.dump(daily, file)

    def test_getAllDataFromWebStorage_load(self):
        print(getMeanOfDaySeriesPerYear(json.load(open('daily.json')), 9))

    def test_getLatestDataFromWebStorage(self):
        daily = getLatestDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        with open('daily.json', 'w') as file:
            json.dump(daily, file)
        # print(getDaysSeries(json.load(open('daily.json'))))
