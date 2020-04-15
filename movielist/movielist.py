# coding: utf-8
#!/usr/local/bin/python3
import datetime
import os
import sys
from bottle import route, run, template, static_file, get, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import movielistdb

@route('/')
def index():
    return template('index.html')

@route('/unwatchedlist')
def unwatchedlist():
    return template('unwatchedlist.html', movielist=movielistdb.read_unwatched())

@route('/edittitle', method="POST")
def edittitle():
    try:
        return template('edittitle.html',
        id=request.POST.getunicode('id'),
        release_year=request.POST.getunicode('release_year'),
        chrome_type=request.POST.getunicode('chrome_type'),
        youga_houga=request.POST.getunicode('youga_houga'),
        acquisition_type=request.POST.getunicode('acquisition_type'),
        title=request.POST.getunicode('title'),
        target=request.POST.getunicode('target'))
    except Exception as e:
        return str(e)

@route('/edittitle2', method="POST")
def edittitle2():
    try:
        youga_houga = request.POST.getunicode('youga_houga')
        if youga_houga == 'youga':
            youga_houga = '洋'
        elif youga_houga == 'houga':
            youga_houga = '邦'

        chrome_type = request.POST.getunicode('chrome_type')
        if chrome_type == 'color':
            chrome_type = 'カ'
        elif chrome_type == 'monochrome':
            chrome_type = 'モ'

        target = request.POST.getunicode('target')
        if target and target == 'on':
            target = 1
        else:
            target = 0

        sql, rows = movielistdb.update(
            id=request.POST.getunicode('id'),
            release_year=request.POST.getunicode('release_year'),
            youga_houga=youga_houga,
            chrome_type=chrome_type,
            acquisition_type=request.POST.getunicode('acquisition_type'),
            title=request.POST.getunicode('title'),
            target=target)
        return template('edittitle2.html',
            sql=sql,
            rows=rows,
            id=request.POST.getunicode('id'),
            release_year=request.POST.getunicode('release_year'),
            youga_houga=youga_houga,
            chrome_type=chrome_type,
            acquisition_type=request.POST.getunicode('acquisition_type'),
            title=request.POST.getunicode('title'),
            target=target)
    except Exception as e:
        return str(e)

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
