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

def add(date, mail_count):
    query("insert into sm_count values ('%s', %s)" % (date, mail_count))

def read_data():
    daily_data = {}
    rows = query('select date, mail_count from sm_count')
    for row in rows:
        date = datetime.datetime.combine(row[0], datetime.time())
        daily_data[date] = int(row[1])
    return daily_data

######################################################################
# test code
######################################################################

class CoronaDBTest(unittest.TestCase):
    def test_read_data(self):
        daily_data = read_data()
        self.assertTrue(len([day.strftime('%Y/%m/%d') for day in daily_data]))
        self.assertTrue(len(list(daily_data.values())) > 0)


if __name__ == '__main__':
    unittest.main()
