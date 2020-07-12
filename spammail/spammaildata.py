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

def add(date, mail_count):
    query("insert into sm_count values ('%s', %s)" % (date, mail_count))

def read_data_recent():
    rows = query('select * from sm_count order by date desc limit 5;')
    return [(date.strftime('%Y/%m/%d'), count) for date, count in rows]

def read_data_daily():
    daily_data = {}
    rows = query('select date, count from sm_count')
    for row in rows:
        date = datetime.datetime.combine(row[0], datetime.time())
        daily_data[date] = int(row[1])
    return daily_data

def read_data_monthly():
    monthly_data = {}
    rows = query("select DATE_FORMAT(date, '%Y/%m') as yearmonth, sum(count) "
                 "from sm_count group by yearmonth")
    for row in rows:
        date = datetime.datetime.strptime(row[0], '%Y/%m')
        if date.year not in monthly_data:
            monthly_data[date.year] = [0] * 12
        monthly_data[date.year][date.month - 1] = int(row[1])
    return monthly_data

def read_data_annually():
    annually_data = {}
    rows = query("select DATE_FORMAT(date, '%Y') as year, sum(count) from sm_count group by year")
    for row in rows:
        annually_data[int(row[0])] = int(row[1])
    return annually_data

######################################################################
# test code
######################################################################

class CoronaDBTest(unittest.TestCase):
    def test_read_data_recent(self):
        print(read_data_recent())

    def test_read_data(self):
        daily_data = read_data_daily()
        self.assertTrue(len([day.strftime('%Y/%m/%d') for day in daily_data]) >= 0)
        self.assertTrue(len(list(daily_data.values())) >= 0)

    def test_read_data_monthly(self):
        monthly_data = read_data_monthly()
        print(monthly_data)

    def test_read_data_annually(self):
        annually_data = read_data_annually()
        print(list(annually_data.keys()))

# python3 -m unittest spammaildata.CoronaDBTest.test_read_data_recent
