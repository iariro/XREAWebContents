'''
database access
'''
import datetime
import MySQLdb
import unittest

def query(sql):
    '''
    :param sql: SQL string
    '''
    conn = MySQLdb.connect(user='iariro', passwd='abc123', host='localhost', db='iariro', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return rows

def add(date, infect_num):
    query("insert into cr_infect values ('%s', %s)" % (date, infect_num))

def read_data():
    daily_data = {}
    sql = 'select date, infect_num from cr_infect'
    rows = query(sql)
    for row in rows:
        date = datetime.datetime.combine(row[0], datetime.time())
        daily_data[date] = int(row[1])
    return daily_data

def read_last_data(limit):
    daily_data = {}
    sql = 'select date, infect_num from cr_infect order by date desc limit %d;' % limit
    rows = query(sql)
    for row in rows:
        daily_data[row[0]] = int(row[1])
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
        weeks, weekly_data = statistic_weekly(daily_data, datetime.datetime(2020, 3, 2), datetime.datetime(2020, 4, 13))
        self.assertTrue(len(weekly_data) > 0)

    def test_sum_weekly(self):
        daily_data = read_data()
        self.assertTrue(len(sum_weekly(daily_data)) > 0)

    def test_last_complete_week_start(self):
        for day, start in {19: 19, 20: 19, 25: 19, 26: 26, 27: 26, 28: 26}.items():
            self.assertEqual(datetime.datetime(2020, 4, start),
                             last_complete_week_start(datetime.datetime(2020, 4, day)))

def test_last_complete_week_start():
    for day, start in {19: 19, 20: 19, 25: 19, 26: 26, 27: 26, 28: 26}.items():
        assert datetime.datetime(2020, 4, start) == last_complete_week_start(datetime.datetime(2020, 4, day))


if __name__ == '__main__':
    unittest.main()
