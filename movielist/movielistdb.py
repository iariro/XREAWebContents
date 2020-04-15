# coding: utf-8
import MySQLdb
import sys, io

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

def read_all():
    rows = query('select * from mv_title where watch_date is not null;')
    titles = []
    for row in rows:
        if row[5]:
            year = row[5].year
            titles_target_year = None
            for titles_year in titles:
                if titles_year['year'] == year:
                    titles_target_year = titles_year
                    break
            if titles_target_year == None:
                titles_target_year = {'year': year, 'titles': []}
                titles.append(titles_target_year)
            titles_target_year['titles'].append({'release_year': row[1], 'youga_houga': row[2], 'chrome_type': row[3], 'acquisition_type': row[4], 'watch_date': str(row[5]), 'title': row[6]})
    return titles

def read_unwatched():
    rows = query('select * from mv_title where watch_date is null;')
    titles = []
    for row in rows:
        titles.append({'id': row[0], 'release_year': row[1], 'youga_houga': row[2], 'chrome_type': row[3], 'acquisition_type': row[4], 'watch_date': str(row[5]), 'title': row[6], 'target': row[7]})
    return titles

def get_monthly_count(years, get_key):
    keys = []
    for year in years:
        for title in year['titles']:
            key = get_key(title)
            if key not in keys:
                keys.append(key)

    month_labels = []
    monthly_count = {}
    for year in years:
        month_labels = ['%d/%02d' % (year['year'], i+1) for i in range(0, 12)] + month_labels
        for key in keys:
            monthly_count[key] = [0] * 12 + (monthly_count[key] if key in monthly_count else [])
        for title in year['titles']:
            key = get_key(title)
            monthly_count[key][int(title['watch_date'][5:7])-1] += 1

    return month_labels, [{'name': key, 'data': value} for key, value in monthly_count.items()]

def get_annual_count(years, get_key):
    keys = []
    for year in years:
        for title in year['titles']:
            key = get_key(title)
            if key not in keys:
                keys.append(key)

    year_labels = []
    year_count = {}
    for year in years:
        year_labels = [year['year']] + year_labels
        for key in keys:
            year_count[key] = [0] + (year_count[key] if key in year_count else [])
        for title in year['titles']:
            key = get_key(title)
            year_count[key][0] += 1

    return year_labels, [{'name': key, 'data': value} for key, value in year_count.items()]

def update(id, release_year, youga_houga, chrome_type, acquisition_type, title, target):
    sql = "SET SQL_SAFE_UPDATES=0; update iariro.mv_title set release_year={}, youga_houga='{}', chrome_type='{}', acquisition_type='{}', title='{}', target={} where id={};".format(release_year, youga_houga, chrome_type, acquisition_type, title, target, id)
    rows = query(sql)
    return sql, rows

if __name__ == '__main__':
    #print(read_unwatched())
    #years = read_all()
    #month_labels, monthly = get_monthly_count(years, lambda title: '月ごと視聴数')
    #month_labels, monthly_count = get_monthly_count(years, lambda title: title['youga_houga'])
    #print(month_labels)
    #print(monthly_count)
    #year_labels, year_count = get_annual_count(years, lambda title: '年ごと視聴数')
    #print(year_labels)
    #print(year_count)
    print(update(191, '2008', 'youga', 'color', 'NR', 'happening', 1))

