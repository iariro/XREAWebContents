# coding: utf-8
import sys
import io
import datetime
import MySQLdb
import unittest

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def query(sql):
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

def extend_chrome_type(code):
    chrome_types = {
        "モ": "モノクロ",
        "カ": "カラー"}
    if code in chrome_types:
        return chrome_types[code]
    else:
        return ''

def extend_acquisition_type(code):
    acquisition_types = {
        "DR": "DVDレンタル",
        "DP": "DVD購入",
        "DA": "DVDオークション",
        "NR": "ネットレンタル",
        "TV": "TV視聴",
        "VA": "VHSオークション",
        "LP": "LD購入",
        "DB": "ひとのDVD"}
    if code in acquisition_types:
        return acquisition_types[code]
    else:
        return ''

def scatter():
    rows = query('select release_year, watch_date, acquisition_type, title '
                 'from mv_title where watch_date is not null;')
    titles = []
    for row in rows:
        acquisition_type = extend_acquisition_type(row[2])
        item = None
        for item2 in titles:
            if item2['name'] == acquisition_type:
                item = item2
                break
        if item is None:
            item = {'name': acquisition_type, 'data': []}
            titles.append(item)
        item['data'].append({
            'x': int(datetime.datetime.combine(row[1], datetime.time()).timestamp()) * 1000,
            'y': int(datetime.datetime(year=row[0], month=1, day=1).timestamp()) * 1000,
            'name': row[3]})
    return titles

def read_watched_title():
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, '
                 'watch_date, title, target '
                 'from mv_title '
                 'where watch_date is not null '
                 'order by watch_date desc, release_year desc;')
    titles = []
    for row in rows:
        if row[5]:
            youga_houga = row[2]
            if youga_houga:
                youga_houga += '画'
            year = row[5].year
            titles_target_year = None
            for titles_year in titles:
                if titles_year['year'] == year:
                    titles_target_year = titles_year
                    break
            if titles_target_year is None:
                titles_target_year = {'year': year, 'titles': []}
                titles.append(titles_target_year)
            chrome_type = extend_chrome_type(row[3])
            acquisition_type = extend_acquisition_type(row[4])
            titles_target_year['titles'].append({'release_year': row[1],
                                                 'youga_houga': youga_houga,
                                                 'chrome_type': chrome_type,
                                                 'acquisition_type': acquisition_type,
                                                 'watch_date': row[5].strftime('%Y/%m/%d'),
                                                 'title': row[6]})
    return titles

def read_unwatched_title(target):
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, title, '
                 'target '
                 'from mv_title '
                 'where watch_date is null '
                 '%s order by release_year' % ('and target=1' if target else ''))
    titles = []
    count = {'total': 0, 'target': 0}
    for row in rows:
        count['total'] += 1
        if row[6] is None:
            target = None
        else:
            target = int.from_bytes(row[6].encode(), 'little')
            if target == 0:
                target = None
            else:
                count['target'] += 1
        youga_houga = row[2]
        if youga_houga:
            youga_houga += '画'
        titles.append({'id': row[0],
                       'release_year': row[1],
                       'youga_houga': youga_houga,
                       'chrome_type': row[3],
                       'acquisition_type': row[4],
                       'title': row[5],
                       'target': target})
    return titles, count

def get_monthly_count(years, get_key):
    keys = []
    for year in years:
        for title in year['titles']:
            key = get_key(title)
            if key not in keys:
                keys.append(key)

    total = 0
    sum = {key: {'count': 0, 'ratio': 0} for key in keys}
    month_labels = []
    monthly_count = {}
    monthly_accum = []
    for year in years:
        month_labels = ['%d/%02d' % (year['year'], i + 1) for i in range(0, 12)] + month_labels
        for key in keys:
            monthly_count[key] = [0] * 12 + (monthly_count[key] if key in monthly_count else [])
        monthly_accum_1year = [0] * 12
        for title in year['titles']:
            total += 1
            key = get_key(title)
            sum[key]['count'] += 1
            month = int(title['watch_date'][5:7])
            monthly_count[key][month - 1] += 1
            monthly_accum_1year[month - 1] += 1
        monthly_accum = monthly_accum_1year + monthly_accum
    for key, value in sum.items():
        value['ratio'] = '%2.2f' % (value['count'] * 100 / total)
    accum = 0
    for i, n in enumerate(monthly_accum):
        monthly_accum[i] = accum + monthly_accum[i]
        accum = monthly_accum[i]
    monthly_count = [{'name': key, 'data': value, 'yAxis': 0} for key, value in monthly_count.items()]
    total = get_all_count()
    monthly_count.append({'name': 'コンプリート率',
                          'data': [round(n * 100 / total, 3) for n in monthly_accum],
                          'type': 'line',
                          'yAxis': 1})

    return month_labels, sum, monthly_count

def get_annual_count(years, get_key):
    keys = []
    for year in years:
        for title in year['titles']:
            key = get_key(title)
            if key not in keys:
                keys.append(key)

    total = 0
    sum = {key: {'count': 0, 'ratio': 0} for key in keys}
    year_labels = []
    year_count = {}
    annual_accum = []
    for year in years:
        year_labels = [year['year']] + year_labels
        for key in keys:
            year_count[key] = [0] + (year_count[key] if key in year_count else [])
        for title in year['titles']:
            total += 1
            key = get_key(title)
            sum[key]['count'] += 1
            year_count[key][0] += 1
        annual_accum.insert(0, len(year['titles']))
    for key, value in sum.items():
        value['ratio'] = '%2.2f' % (value['count'] * 100 / total)

    accum = 0
    for i, n in enumerate(annual_accum):
        annual_accum[i] = accum + annual_accum[i]
        accum = annual_accum[i]

    year_count = [{'name': key, 'data': value} for key, value in year_count.items()]
    total = get_all_count()
    year_count.append({'name': 'コンプリート率',
                       'data': [round(n * 100 / total, 3) for n in annual_accum],
                       'type': 'line',
                       'yAxis': 1})

    return year_labels, sum, year_count

def string_or_null(value):
    if value is None:
        return 'null'
    else:
        return "'%s'" % value

def update(id, release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target):
    sql = "SET SQL_SAFE_UPDATES=0; " \
          "update iariro.mv_title " \
          "set release_year={}, youga_houga={}, chrome_type={}, acquisition_type={}, " \
          "watch_date={}, title={}, " \
          "target={} " \
          "where id={};".format(release_year,
                                string_or_null(youga_houga),
                                string_or_null(chrome_type),
                                string_or_null(acquisition_type),
                                string_or_null(watch_date),
                                string_or_null(title),
                                target,
                                id)
    rows = query(sql)
    return sql, rows

def get_all_count():
    rows = query('select count(*) from mv_title;')
    return rows[0][0]

def add_title(release_year=None, youga_houga=None, chrome_type=None, acquisition_type=None, watch_date=None, title=None, target=None):
    values = []
    values.append(str(release_year) if release_year else 'null')
    values.append("'{}'".format(youga_houga) if youga_houga else 'null')
    values.append("'{}'".format(chrome_type) if chrome_type else 'null')
    values.append("'{}'".format(acquisition_type) if acquisition_type else 'null')
    values.append("'{}'".format(watch_date) if watch_date else 'null')
    values.append("'{}'".format(title) if title else 'null')
    values.append(str(target) if target else 'null')
    sql = "insert into mv_title " \
          "(release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target) " \
          "values ({});".format(','.join(values))
    query(sql)

################################################################################

class MovielistdbTest(unittest.TestCase):

    def test_extend_chrome_type(self):
        self.assertEqual("モノクロ", extend_chrome_type("モ"))
        self.assertEqual("カラー", extend_chrome_type("カ"))

    def test_extend_acquisition_type(self):
        self.assertEqual("DVDレンタル", extend_acquisition_type("DR"))
        self.assertEqual("DVD購入", extend_acquisition_type("DP"))
        self.assertEqual("DVDオークション", extend_acquisition_type("DA"))
        self.assertEqual("ネットレンタル", extend_acquisition_type("NR"))
        self.assertEqual("TV視聴", extend_acquisition_type("TV"))
        self.assertEqual("VHSオークション", extend_acquisition_type("VA"))
        self.assertEqual("LD購入", extend_acquisition_type("LP"))
        self.assertEqual("ひとのDVD", extend_acquisition_type("DB"))

    def test_scatter(self):
        self.assertTrue(len(scatter()) > 0)

    def test_read_watched_title(self):
        self.assertTrue(len(read_watched_title()) > 0)

    def test_read_unwatched_title(self):
        titles, count = read_unwatched_title(False)
        self.assertTrue(len(titles) > 0)

    def test_get_monthly_count(self):
        years = read_watched_title()
        month_labels, sum, arr = get_monthly_count(years, lambda title: title['youga_houga'])
        print(arr)
        self.assertTrue(len(month_labels) > 0)
        self.assertIsNotNone(sum)
        self.assertTrue(len(arr) > 0)

    def test_get_annual_count(self):
        years = read_watched_title()
        year_labels, sum, arr = get_annual_count(years, lambda title: title['youga_houga'])
        print(arr)
        self.assertTrue(len(year_labels) > 0)
        self.assertIsNotNone(sum)
        self.assertTrue(len(arr) > 0)

    def test_string_or_null(self):
        self.assertEqual('null', string_or_null(None))
        self.assertEqual("'abc'", string_or_null('abc'))

#   def test_update(self):
#       update(id, release_year, youga_houga, chrome_type, acq_type, watch_date, title, target)

    def test_get_all_count(self):
        print('test_get_all_count')
        print(get_all_count())

    def test_add_title(self):
        add_title(release_year=2000,
                  youga_houga='洋',
                  title='test')


# python3 -m unittest movielistdb.py movielistdb.MovielistdbTest.test_get_all_count
