# coding: utf-8
import sys
import io
import datetime
import MySQLdb

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def query(sql):
    conn = MySQLdb.connect(user='iariro', passwd='abc123', host='localhost', db='iariro', charset='utf8')
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
    rows = query('select release_year, watch_date, acquisition_type, title from mv_title where watch_date is not null;')
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
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target ' \
                 'from mv_title ' \
                 'where watch_date is not null ' \
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
            titles_target_year['titles'].append({'release_year': row[1],
                                                 'youga_houga': youga_houga,
                                                 'chrome_type': extend_chrome_type(row[3]),
                                                 'acquisition_type': extend_acquisition_type(row[4]),
                                                 'watch_date': str(row[5]),
                                                 'title': row[6]})
    return titles

def read_unwatched_title(target):
    rows = query('select id, release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target ' \
                 'from mv_title ' \
                 'where watch_date is null %s order by release_year' % ('and target=1' if target else ''))
    titles = []
    count = {'total': 0, 'target': 0}
    for row in rows:
        count['total'] += 1
        if row[7] is None:
            target = None
        else:
            target = int.from_bytes(row[7].encode(), 'little')
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
                       'watch_date': str(row[5]),
                       'title': row[6],
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
    for year in years:
        month_labels = ['%d/%02d' % (year['year'], i + 1) for i in range(0, 12)] + month_labels
        for key in keys:
            monthly_count[key] = [0] * 12 + (monthly_count[key] if key in monthly_count else [])
        for title in year['titles']:
            total += 1
            key = get_key(title)
            sum[key]['count'] += 1
            monthly_count[key][int(title['watch_date'][5:7]) - 1] += 1
    for key, value in sum.items():
        value['ratio'] = '%2.2f' % (value['count'] * 100 / total)

    return month_labels, sum, [{'name': key, 'data': value} for key, value in monthly_count.items()]

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
    for year in years:
        year_labels = [year['year']] + year_labels
        for key in keys:
            year_count[key] = [0] + (year_count[key] if key in year_count else [])
        for title in year['titles']:
            total += 1
            key = get_key(title)
            sum[key]['count'] += 1
            year_count[key][0] += 1
    for key, value in sum.items():
        value['ratio'] = '%2.2f' % (value['count'] * 100 / total)

    return year_labels, sum, [{'name': key, 'data': value} for key, value in year_count.items()]

def string_or_null(value):
    if value is None:
        return 'null'
    else:
        return "'%s'" % value

def update(id, release_year, youga_houga, chrome_type, acquisition_type, watch_date, title, target):
    sql = "SET SQL_SAFE_UPDATES=0; " \
          "update iariro.mv_title " \
          "set release_year={}, youga_houga={}, chrome_type={}, acquisition_type={}, watch_date={}, title={}, " \
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


if __name__ == '__main__':
    # print(scatter()[0])
    # print(read_watched_title())
    years = read_watched_title()
    print(read_unwatched_title(True))
    # month_labels, monthly = get_monthly_count(years, lambda title: '月ごと視聴数')
    # month_labels, sum, monthly_count = get_monthly_count(years, lambda title: title['chrome_type'])
    # print(month_labels)
    # print(monthly_count)
    # year_labels, sum, year_count = get_annual_count(years, lambda title: '年ごと視聴数')
    # print(year_labels)
    # print(year_count)
    # print(update(191, '2008', 'youga', 'color', 'NR', 'happening', 1))
