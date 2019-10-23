import datetime
import json
import urllib.request
from statistics import mean

def getLatestDataFromWebStorage():
    url = 'https://api.webstorage.jp/v1/devices/latest-data'
    data = {"api-key":"j8j04n070kccokm8c7odoa89m6tjbi0qt69o4k8dac1n1","login-id": "tbac0004","login-pass": "bukkuden", "remote-serial": "5214C18D"}
    headers = {
        'Content-Type': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }

    days = {}
    months = {}
    weeks = {}
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()
        js = json.loads(body.decode())
        for row in js['data']:
            dt = datetime.datetime.fromtimestamp(int(row['unixtime']))
            date = dt.strftime('%Y/%m/%d')
            if date not in days:
                days[date] = [None] * 24
            temp = float(row['ch1'])
            days[date][dt.hour] = temp

            week = (dt - datetime.timedelta(days=dt.weekday())).strftime('%Y/%m/%d')
            if week not in weeks:
                weeks[week] = []
            weeks[week].append(temp)

            month = datetime.date(dt.year, dt.month, 1).strftime('%Y/%m/%d')
            if month not in months:
                months[month] = []
            months[month].append(temp)
    return (days, months, weeks)

def getDaysSeries(days):
    return ','.join(["{name:'%s', data:%s}" % (date, [temp for temp in temps if temp]) for date, temps in sorted(days.items())[-5:]])

def getMeanOfDaySeries(days):
    return ','.join(["[%d, %d]" % (datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000, mean([temp for temp in temps if temp])) for date, temps in sorted(days.items())])

def getMaxOfDaySeries(days):
    return ','.join(["[%d, %d]" % (datetime.datetime.strptime(date, '%Y/%m/%d').timestamp() * 1000, max([temp for temp in temps if temp])) for date, temps in sorted(days.items())])

def getWeeksSeries(weeks):
    return ''

if __name__ == '__main__':
#   (days, months, weeks) = getLatestDataFromWebStorage()
#   with open('days.json', 'w') as file:
#       json.dump(days, file)
#   with open('weeks.json', 'w') as file:
#       json.dump(weeks, file)

#   print(getDaysSeries(json.load(open('days.json'))))

    print(getMaxOfDaySeries(json.load(open('days.json'))))
