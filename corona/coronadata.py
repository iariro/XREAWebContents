import sys
import csv
import datetime

def read_data(start_date, end_date):
	daily_data = {}
	with open('corona.csv') as file:
		reader = csv.reader(open('corona.csv')) 
		header = None
		for row in reader:
			if header is None:
				header = row
				continue
			if start_date <= row[0] <= end_date:
				daily_data[datetime.datetime.strptime(row[0], '%Y/%m/%d')] = int(row[1])
	return daily_data

def statistic_weekly(daily_data):
	weeks = [None] * 7
	weekly_data = {}
	for day, num in daily_data.items():
		weeks[day.weekday()] = day.strftime('%a')
		week_start = day - datetime.timedelta(days=day.weekday())
		if week_start not in weekly_data:
			weekly_data[week_start] = [0] * 7
		weekly_data[week_start][day.weekday()] = num
	for week, values in weekly_data.items():
		weekly_data[week] = [value * 100 / sum(values) for value in values]
	return weeks, weekly_data

if __name__ == '__main__':
	daily_data = read_data(sys.argv[1], sys.argv[2])
	#print([day.strftime('%Y/%m/%d') for day in daily_data])
	#print(list(daily_data.values()))
	weeks, weekly_data = statistic_weekly(daily_data)
	print([{'name': day.strftime('%Y/%m/%d'), 'data': values} for day, values in weekly_data.items()])
