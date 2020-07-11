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

def get_area_count():
    rows = query("SELECT SUBSTRING(address,1, CASE WHEN locate('県',address)<>0 THEN locate('県',address) WHEN locate('府',address)<>0 THEN locate('府',address) WHEN locate('都',address)<>0 THEN locate('都',address) END) as prefecture, count(visit_date), count(*) FROM iariro.ho_store group by prefecture;")

    prefectures = []
    visited = []
    unvisited = []
    for row in rows:
        prefectures.append(row[0])
        visited.append(row[1])
        unvisited.append(row[2])
    return (prefectures, visited, unvisited)

def get_completion_history():
    rows = query("SELECT * FROM ho_store where visit_date is not null;")
    dates = []
    for row in rows:
        dates.append(row['visit_date'])

    monthlycount = array();
    monthlycount2 = array();
    nowyear = datetime.datetime.now().year
    d2 = None
    for year in range(2018, nowyear+2):
        for month in range(1, 12 + 1):
            if year == nowyear+1 and month>1:
                break
            d = datetime.datetime(year=year, month=month, day=1)
            count = 0
            count2 = 0
            for date in dates:
                if date < d:
                    count2 += 1
                    if date >= d2:
                        count += 1

            if d is not None:
                monthlycount[d2] = count
                monthlycount2[d2] = count2
            d2 = d

    bardata = [[month, count] for month, count in monthlycount.items()]
    linedata = [[month, count] for month, count in monthlycount2.items()]

    return bardata, linedata

def update_store(store_id, near_station, minutes_from_near_station, visit_date, address, targeting):
    values = []
    if near_station is None and minutes_from_near_station is not None:
        values.append("near_station='%s'" % near_station)
        values.append("minutes_from_near_station=%d" % minutes_from_near_station)

    if visit_date is not None:
        values.append("visit_date='%s'" % visit_date)
    else:
        values.append("visit_date=null")

    if address is not None:
        values.append("address='%s'" % address)
    else:
        values.append("visit_date=null")

    if targeting is not None:
        values.append("targeting='target'")
    else:
        values.append("targeting=null")

    query("update ho_store set %s where store_id=%d" % (','.join(values), store_id))

def get_store_list(where):
    where_clause = {'visited': ' where visit_date is not null',
             'visited_day': ' where visit_date is not null',
             'unvisited': ' where visit_date is null',
             'target': ' where visit_date is null and targeting is not null'}

    sql = "SELECT * FROM ho_store"
    if where in where_clause:
        sql += where[where]
    if where == 'visited_day':
        sql += ' order by visit_date desc'

    pday = None
    rows = query(sql)
    days = []
    day = None
    for row in rows:
        if where == 'visited_day' and pday != None and pday != row["visit_date"]:
            day = {'date': row["visit_date"], 'values': []}
            days.append(day)
        day['values'].append(row)
    return len(rows), days

def update_visit_date():
    today = dateime.datetime.now().strftime('%Y/%m/%d')

    sql = "update ho_store set visit_date='%s' where store_id=%d" % (today, store_id)
    query(sql)

######################################################################
# test code
######################################################################

class HardoffDBTest(unittest.TestCase):
    def test_get_area_count(self):
        get_area_count()

    def test_get_completion_history(self):
        get_completion_history()

#   def test_update_store(self):
#       update_store(store_id, near_station, minutes_from_near_station, visit_date, targeting)

    def test_get_store_list(self):
        get_store_list(where)

#   def test_update_visit_date(self):
#       update_visit_date()
