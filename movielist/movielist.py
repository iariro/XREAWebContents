#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, run, template, static_file, get
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import movielistdb

@route('/')
def index():
    return template('index.html')

@route('/titlelist')
def titlelist():
    return template('titlelist.html', movielist=movielistdb.read_all())

@route('/histgram')
def histgram():
    return template('histgram.html', histgram=movielistdb.histgram())

@route('/annual_graph_all')
def annual_graph_all():
    years = movielistdb.read_all()
    year_labels, year_count = movielistdb.get_annual_count(years, lambda title: '年ごと視聴数')
    return template('histgram.html', month_labels=year_labels, monthly_count=year_count )
    return str(e)

@route('/monthly_graph_all')
def monthly_graph_all():
    years = movielistdb.read_all()
    month_labels, monthly_count = movielistdb.get_monthly_count(years, lambda title: '月ごと視聴数')
    return template('histgram.html', month_labels=month_labels, monthly_count=monthly_count )
    return str(e)

@route('/monthly_graph_by_category')
def monthly_graph_by_category():
    years = movielistdb.read_all()
    month_labels, monthly_count = movielistdb.get_monthly_count(years, lambda title: title['youga_houga'])
    return template('histgram.html', month_labels=month_labels, monthly_count=monthly_count )
    return str(e)

@route('/monthly_graph_by_acquisition_type')
def monthly_graph_by_acquisition_type():
    years = movielistdb.read_all()
    month_labels, monthly_count = movielistdb.get_monthly_count(years, lambda title: title['acquisition_type'])
    return template('histgram.html', month_labels=month_labels, monthly_count=monthly_count )

@route('/monthly_graph_by_chrome_type')
def monthly_graph_by_chrome_type():
    years = movielistdb.read_all()
    month_labels, monthly_count = movielistdb.get_monthly_count(years, lambda title: title['chrome_type'])
    return template('histgram.html', month_labels=month_labels, monthly_count=monthly_count )
