'''
database access
'''
import datetime
import MySQLdb
import unittest
import urllib.request
import csv

def query(sql):
    '''
    :param sql: SQL string
    '''
    conn = MySQLdb.connect(user='iariro',
                           passwd='abc123',
                           host='localhost',
                           db='iariro',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return rows

def add(date, infect_num):
    query("insert into cr_infect values ('%s', %s)" % (date, infect_num))

def update(date, infect_num):
    query("update cr_infect set infect_num=%s where date='%s';" % (infect_num, date))

def read_data():
    daily_data = {}
    sql = 'select date, infect_num from cr_infect'
    rows = query(sql)
    for row in rows:
        date = datetime.datetime.combine(row[0], datetime.time())
        daily_data[date] = int(row[1])
    return daily_data

def read_mhlw_data():
    ''' 厚労省のデータを取得'''
    with urllib.request.urlopen('https://www.mhlw.go.jp/content/pcr_positive_daily.csv') as res:
        body = res.read()
        daily_data = {}
        for row in csv.reader(body.decode().splitlines()[1:]):
            try:
                daily_data[datetime.datetime.strptime(row[0], '%Y/%m/%d')] = int(row[1])
            except ValueError as error:
                pass
    return daily_data

def read_last_data(limit):
    daily_data = {}
    sql = 'select date, infect_num from cr_infect order by date desc limit %d;' % limit
    rows = query(sql)
    for row in rows:
        daily_data[row[0].strftime('%Y/%m/%d')] = int(row[1])
    return daily_data

def sum_weekly(daily_data):
    weekly_data = {}
    for day, num in daily_data.items():
        week_start = day - datetime.timedelta(days=day.weekday())
        if week_start not in weekly_data:
            weekly_data[week_start] = []
        weekly_data[week_start].append(num)
    return {week: sum(values) * 7 / len(values) for week, values in weekly_data.items()}

def statistic_weekly(daily_data, start_date, end_date):
    weeks = [None] * 7
    weekly_data = {}
    for day, num in daily_data.items():
        if start_date <= day <= end_date:
            weeks[day.weekday()] = day.strftime('%a')
            week_start = day - datetime.timedelta(days=day.weekday())
            if week_start not in weekly_data:
                weekly_data[week_start] = [0] * 7
            weekly_data[week_start][day.weekday()] = num
    for week, values in weekly_data.items():
        weekly_data[week] = [value * 100 / sum(values) for value in values]
    return weeks, weekly_data

def statistic_weekday(daily_data, start_date, end_date):
    d = datetime.datetime.today()
    while d.weekday() > 0:
        d += datetime.timedelta(days=1)
    weeks = {}
    weekday_date = []
    for i in range(7):
        weeks[d.strftime('%a')] = []
        d += datetime.timedelta(days=1)
    for day, num in daily_data.items():
        if start_date <= day <= end_date:
            week_start = (day - datetime.timedelta(days=day.weekday())).strftime('%Y/%m/%d')
            if week_start not in weekday_date:
                weekday_date.append(week_start)
            weeks[day.strftime('%a')].append(num)
    return weekday_date, weeks

def last_complete_week_start(date):
    date += datetime.timedelta(days=1)
    date -= datetime.timedelta(days=date.weekday())
    return date - datetime.timedelta(days=1)

######################################################################
# test code
######################################################################

class CoronaDBTest(unittest.TestCase):
    def test_read_data(self):
        daily_data = read_data()
        self.assertTrue(len([day.strftime('%Y/%m/%d') for day in daily_data]))
        self.assertTrue(len(list(daily_data.values())) > 0)

    def test_read_data_limit(self):
        daily_data = read_last_data(5)
        self.assertTrue(len(list(daily_data.values())) == 5)

    def test_statistic_weekly(self):
        daily_data = read_data()
        weeks, weekly_data = statistic_weekly(daily_data,
                                              datetime.datetime(2020, 3, 2),
                                              datetime.datetime(2020, 4, 13))
        self.assertTrue(len(weekly_data) > 0)

    def test_sum_weekly(self):
        daily_data = read_data()
        self.assertTrue(len(sum_weekly(daily_data)) > 0)

    def test_last_complete_week_start(self):
        for day, start in {19: 19, 20: 19, 25: 19, 26: 26, 27: 26, 28: 26}.items():
            self.assertEqual(datetime.datetime(2020, 4, start),
                             last_complete_week_start(datetime.datetime(2020, 4, day)))

    def test_read_mhlw_data(self):
        print(read_mhlw_data())

    def test_statistic_weekday(self):
        daily_data = read_data()
        print(statistic_weekday(daily_data,
                                datetime.datetime(2020, 3, 2),
                                datetime.datetime(2020, 8, 3)))

def test_last_complete_week_start():
    for day, start in {19: 19, 20: 19, 25: 19, 26: 26, 27: 26, 28: 26}.items():
        assert datetime.datetime(2020, 4, start) == \
            last_complete_week_start(datetime.datetime(2020, 4, day))

# python3 -m unittest coronadata.CoronaDBTest.test_read_mhlw_data
