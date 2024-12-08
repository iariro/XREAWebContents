import datetime
import json
import urllib.request
from statistics import mean
import unittest

apikey = "j8j04n070kccokm8c7odoa89m6tjbi0qt69o4k8dac1n1"

def getCurrentDataFromWebStorage(login_id, login_pass):
    '''デバイスリストを取得

        Args:
            login_id: ログインID
            login_pass: パスワード

        Returns:
            {'devices': [{ ... }]}
    '''
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
    '''指定デバイスの全温度データを取得

        Args:
            login_id: ログインID
            login_pass: パスワード
            remote_serial: デバイスシリアル

        Returns:
            (monthly, weekly, daily)
    '''
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
            if row['ch1'].startswith('E'):
                continue

            temp = float(row['ch1'])
            if temp >= 100:
                continue

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
    '''指定デバイスの直近温度データを取得

        Args:
            login_id: ログインID
            login_pass: パスワード
            remote_serial: デバイスシリアル

        Returns:
            {date: {hour: temp}}
    '''
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
            if row['ch1'].startswith('E') == False:
                temp = float(row['ch1'])
                if temp < 100:
                    daily[date][dt.hour] = temp
    return daily

def getDaysSeries(days):
    '''直近５日分グラフデータ生成

        Args:
            days: getLatestDataFromWebStorage()の出力

        Returns:
            {date: {hour: temp}}
    '''
    return ','.join(["{name:'%s', data:%s}" % (date[5:], [temp for temp in temps if temp])
                    for date, temps in sorted(days.items())[-5:]])

def to_unixtime(date):
    '''Highcharts用時刻値に変換

        Args:
            date: YYYY/mm/dd形式の日付

        Returns:
            Highcharts用時刻値
    '''
    return datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000

def getProcessedDaySeries(days, proc):
    '''最高気温・最低気温等に加工した配列を生成する

        Args:
            days: getLatestDataFromWebStorage()の出力
            proc: 値を加工する関数

        Returns:
            [時刻, 温度], [時刻, 温度] ...
    '''
    arr = [(date, proc([temp for temp in temps if temp])) for date, temps in sorted(days.items())]
    return ','.join(["[%d, %.2f]" % (to_unixtime(date), temp) for date, temp in arr])

def getMeanOfDaySeriesPerYear(daily, start_date=None, mean_range=9):
    ''' 年ごとの推移を取得。推移は移動平均する。

        Args:
            daily: { date: [temp] }
            start_date: データ取得開始日
            mean_range: 移動平均する日数

        Returns:
            { 'name': year, 'data': [[datetime, temp]] }
    '''
    today = datetime.datetime.today().strftime('%Y/%m/%d')
    if today in daily:
        if len(daily[today]) < 24:
            del daily[today]

    # 平均気温
    for day in daily:
        if day != today or len(daily[today]) == 24:
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
        if start_date is None or day >= start_date:
            years[day[:4]][day[5:]] = value
    series = []
    for year in years:
        data = [[to_unixtime(today[0:4] + '/' + date), value] for date, value in years[year].items()]
        series.append({'name': '%s年' % year,
                       'data': data})
    return series

####################################################################################################

class TestOndotoriData(unittest.TestCase):
    def test_getCurrentDataFromWebStorage(self):
        print(getCurrentDataFromWebStorage('tbac0004', 'bukkuden'))

    def test_getAllDataFromWebStorage_dump(self):
        (monthly, weekly, daily) = getAllDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        with open('data/monthly.json', 'w') as file:
            json.dump(monthly, file)
        with open('data/weekly.json', 'w') as file:
            json.dump(weekly, file)
        with open('data/daily.json', 'w') as file:
            json.dump(daily, file)

    def test_getAllDataFromWebStorage_load(self):
        print(getMeanOfDaySeriesPerYear(json.load(open('data/daily.json')),
                                        start_date='2019/07/01',
                                        mean_range=9))

    def test_getLatestDataFromWebStorage(self):
        daily = getLatestDataFromWebStorage('tbac0004', 'bukkuden', '5214C18D')
        with open('data/daily.json', 'w') as file:
            json.dump(daily, file)
        print(getDaysSeries(json.load(open('data/daily.json'))))
