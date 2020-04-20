import sys
import csv
import datetime
import MySQLdb

def query(sql):
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
	rows = query('select date, infect_num from cr_infect')
	for row in rows:
		date = datetime.datetime.combine(row[0], datetime.time())
		daily_data[date] = int(row[1])
	return daily_data

def statistic_weekly(daily_data, start_date, end_date):
	start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
	end_date = datetime.datetime.strptime(end_date, '%Y/%m/%d')
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

if __name__ == '__main__':
	daily_data = read_data()
	#print([day.strftime('%Y/%m/%d') for day in daily_data])
	#print(list(daily_data.values()))
	weeks, weekly_data = statistic_weekly(daily_data, sys.argv[1], sys.argv[2])
	print([{'name': day.strftime('%Y/%m/%d'), 'data': values} for day, values in weekly_data.items()])
