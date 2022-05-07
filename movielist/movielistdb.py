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

def read_all():
    titles = []
    rows = query('select * from mv_title order by watch_date desc, release_year;')
    for row in rows:
        titles.append(row)
    return titles

def scatter(watched):
    sql = 'select release_year, watch_date, acquisition_type, title, insert_date from mv_title '
    if watched:
        sql += 'where watch_date is not null'
    else:
        sql += 'where watch_date is null'
    sql += ' order by insert_date;'
    rows = query(sql)
    titles = []
    for row in rows:
        acquisition_type = extend_acquisition_type(row[2])
        item = None
        if watched:
            name = acquisition_type
        else:
            name = '{}年'.format(row[4].year)
        for item2 in titles:
            if item2['name'] == name:
                item = item2
                break
        if item is None:
            item = {'name': name, 'data': []}
            titles.append(item)

        if watched:
            d = row[1]
        else:
            d = row[4]
        item['data'].append({
            'x': int(datetime.datetime.combine(d, datetime.time()).timestamp()) * 1000,
            'y': int(datetime.datetime(year=row[0], month=1, day=1).timestamp()) * 1000,
            'name': row[3]})
    return titles

def read_watched_title():
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, '
                 'watch_date, title, target, insert_date '
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
                                                 'title': row[6],
                                                 'insert_date': row[8].strftime('%Y/%m/%d')})
    return titles

def read_unwatched_title(target):
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, title, '
                 'target, insert_date '
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
                       'target': target,
                       'insert_date': row[7].strftime('%Y/%m/%d')})
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

def get_balance_count():
    rows = query('select substr(watch_date, 1, 7), substr(insert_date, 1, 7) from mv_title;')
    start_date = None
    end_date = None
    watch_count = {}
    insert_count = {}
    for row in rows:
        if row[0]:
            if start_date is None or start_date > row[0]:
                start_date = row[0]
            if end_date is None or end_date < row[0]:
                end_date = row[0]

            d = datetime.datetime.strptime(row[0], '%Y-%m')
            d = '{}-{:02}'.format(d.year, d.month - (d.month - 1) % 3)
            if d not in watch_count:
                watch_count[d] = 0
            watch_count[d] += 1

        if row[1]:
            if start_date is None or start_date > row[1]:
                start_date = row[1]
            if end_date is None or end_date < row[1]:
                end_date = row[1]

            d = datetime.datetime.strptime(row[1], '%Y-%m')
            d = '{}-{:02}'.format(d.year, d.month - (d.month - 1) % 3)
            if d not in insert_count:
                insert_count[d] = 0
            insert_count[d] += 1

    start_date = datetime.datetime.strptime(start_date + '-01', '%Y-%m-%d')
    start_date = datetime.datetime(start_date.year,
                                   start_date.month - (start_date.month - 1) % 3,
                                   1)
    end_date = datetime.datetime.strptime(end_date + '-01', '%Y-%m-%d')
    label = []
    watch_count2 = []
    watch_count2 = []
    insert_count2 = []
    balance_count = 0
    balance_count2 = []
    total_insert_count = 0
    total_watch_count = 0
    total_insert_count2 = []
    total_watch_count2 = []
    d = start_date
    while d <= end_date:
        if d.month % 3 == 1 and d.day == 1:
            label.append(d.strftime('%Y/%m'))

            watch_count3 = 0
            if d.strftime('%Y-%m') in watch_count:
                watch_count3 = watch_count[d.strftime('%Y-%m')]
            watch_count2.append(watch_count3)
            total_watch_count += watch_count3
            total_watch_count2.append(total_watch_count)

            insert_count3 = 0
            if d.strftime('%Y-%m') in insert_count:
                insert_count3 = insert_count[d.strftime('%Y-%m')]
            insert_count2.append(-insert_count3)
            total_insert_count += insert_count3
            total_insert_count2.append(total_insert_count)

            balance_count += watch_count3 - insert_count3
            balance_count2.append(balance_count)

        d += datetime.timedelta(days=1)

    return label, watch_count2, insert_count2, total_insert_count2, total_watch_count2, balance_count2

def add_title(release_year=None, youga_houga=None, chrome_type=None, acquisition_type=None,
              watch_date=None, title=None, target=None):
    values = []
    values.append(str(release_year) if release_year else 'null')
    values.append("'{}'".format(youga_houga) if youga_houga else 'null')
    values.append("'{}'".format(chrome_type) if chrome_type else 'null')
    values.append("'{}'".format(acquisition_type) if acquisition_type else 'null')
    values.append("'{}'".format(watch_date) if watch_date else 'null')
    values.append("'{}'".format(title) if title else 'null')
    values.append(str(target) if target else 'null')
    values.append('now()')
    sql = "insert into mv_title " \
          "(release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target, insert_date) " \
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

    def test_read_all(self):
        titles = read_all()
        for title in titles:
            id, release_year, yh, chrome, acquisition, watch_date, title, target, insert = title
            if watch_date is None:
                print('\t'.join([str(id), str(release_year), yh, title]))
        for title in titles:
            id, release_year, yh, chrome, acquisition, watch_date, title, target, insert = title
            if watch_date is None:
                continue
            chrome2 = chrome if chrome else '-'
            acquisition2 = acquisition if chrome else '-'
            watch_date2 = watch_date.strftime('%m/%d') if watch_date else '-'
            print('\t'.join([str(id), str(release_year), yh, chrome2, acquisition2, watch_date2, title]))

    def test_scatter(self):
        print(scatter(False))

    def test_read_watched_title(self):
        print(read_watched_title())

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

    def test_get_balance_count(self):
        print(get_balance_count())

# python3 -m unittest movielistdb.MovielistdbTest.test_get_all_count
