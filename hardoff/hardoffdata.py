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
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return rows

def get_area_count():
    rows = query("SELECT SUBSTRING(address,1, CASE "
                 "WHEN locate('県',address)<>0 THEN locate('県',address) "
                 "WHEN locate('府',address)<>0 THEN locate('府',address) "
                 "WHEN locate('都',address)<>0 THEN locate('都',address) END) as prefecture, "
                 "count(visit_date) as count_visit_date, count(*) as count_all "
                 "FROM iariro.ho_store group by prefecture;")

    prefectures = []
    visited = []
    unvisited = []
    for row in rows:
        prefectures.append(row['prefecture'])
        visited.append(row['count_visit_date'])
        unvisited.append(row['count_all'] - row['count_visit_date'])
    return (prefectures, visited, unvisited)

def get_completion_history():
    rows = query("SELECT * FROM ho_store where visit_date is not null;")

    dates = []
    for row in rows:
        dates.append(row['visit_date'])

    monthlycount = {}
    monthlycount2 = {}
    nowyear = datetime.datetime.now().year
    d2 = None
    for year in range(2018, nowyear + 2):
        for month in range(1, 12 + 1):
            if year == nowyear + 1 and month > 1:
                break
            d = datetime.datetime(year=year, month=month, day=1)
            count = 0
            count2 = 0
            for date in dates:
                date = datetime.datetime.combine(date, datetime.time())
                if date < d:
                    count2 += 1
                    if date >= d2:
                        count += 1

            if d2 is not None:
                monthlycount[d2] = count
                monthlycount2[d2] = count2
            d2 = d

    bardata = [[month.timestamp() * 1000, count] for month, count in monthlycount.items()]
    linedata = [[month.timestamp() * 1000, count] for month, count in monthlycount2.items()]

    return bardata, linedata

def update_store(store_id, near_station, minutes_from_near_station, visit_date, address, targeting):
    values = []
    if near_station is not None and minutes_from_near_station is not None:
        values.append("near_station='%s'" % near_station)
        values.append("minutes_from_near_station=%s" % minutes_from_near_station)

    if visit_date is not None:
        values.append("visit_date='%s'" % visit_date)

    if address is not None:
        values.append("address='%s'" % address)

    if targeting is not None and len(targeting) > 0:
        values.append("targeting='target'")

    sql = "update ho_store set %s where store_id=%s" % (','.join(values), store_id)
    query(sql)
    return sql

def get_store_list(where):
    where_clause = {'visited': ' where visit_date is not null',
                    'visited_day': ' where visit_date is not null',
                    'unvisited': ' where visit_date is null',
                    'target': ' where visit_date is null and targeting is not null'}

    sql = "SELECT * FROM ho_store"
    if where in where_clause:
        sql += where_clause[where]
    if where == 'visited_day':
        sql += ' order by visit_date desc'

    pday = None
    rows = query(sql)
    days = []
    day = None
    for row in rows:
        if day is None or \
           (where == 'visited_day' and pday is not None and pday != row["visit_date"]):
            day = {'date': row["visit_date"], 'values': []}
            days.append(day)
        day['values'].append(row)
        pday = row["visit_date"]
    return len(rows), days

def update_visit_date(store_id, date):
    today = date.strftime('%Y/%m/%d')

    sql = "update ho_store set visit_date='%s' where store_id=%s" % (today, store_id)
    query(sql)

######################################################################
# test code
######################################################################

class HardoffDBTest(unittest.TestCase):
    def test_get_area_count(self):
        (prefectures, visited, unvisited) = get_area_count()
        self.assertIsNotNone(get_area_count())

    def test_get_completion_history(self):
        self.assertIsNotNone(get_completion_history())

    def test_update_store(self):
        print(update_store('1', None, None, '2020/07/12', None, None))

    def test_get_store_list_visited(self):
        count, days = get_store_list('visited')
        for day in days:
            print(day['date'])

    def test_get_store_list_visited_day(self):
        count, days = get_store_list('visited_day')
        for day in days:
            print(day['date'])

    def test_get_store_list_unvisited(self):
        count, days = get_store_list('unvisited')
        for day in days:
            print(day['date'])

    def test_get_store_list_target(self):
        count, days = get_store_list('target')
        for day in days:
            print(day['date'])

    def test_update_visit_date(self):
        update_visit_date('1', datetime.date.today())

# python3 -m unittest hardoffdata.HardoffDBTest.
