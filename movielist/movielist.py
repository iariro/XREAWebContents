# coding: utf-8
import datetime
import os
import sys
from bottle import route, template, request
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath)
os.chdir(dirpath)
import movielistdb

@route('/')
def index():
    return template('index.html')

@route('/targetlist')
def targetlist():
    try:
        movielist, count = movielistdb.read_unwatched_title(True)
        return template('simplelist.html', movielist=movielist, count=count)
    except Exception as e:
        return str(e)

@route('/unwatchedlist')
def unwatchedlist():
    try:
        movielist, count = movielistdb.read_unwatched_title(False)
        return template('simplelist.html', movielist=movielist, count=count)
    except Exception as e:
        return str(e)

@route('/watchedlist')
def titlelist():
    try:
        return template('annuallist.html', movielist=movielistdb.read_watched_title())
    except Exception as e:
        return str(e)

@route('/edittitle', method="POST")
def edittitle():
    try:
        target = request.POST.getunicode('target')
        watch_date = request.POST.getunicode('watch_date')
        if watch_date is not None:
            status = 'watched'
        else:
            if target == '1':
                status = 'target'
            else:
                status = 'unwatched'

        return template('edittitle.html',
                        id=request.POST.getunicode('id'),
                        release_year=request.POST.getunicode('release_year'),
                        chrome_type=request.POST.getunicode('chrome_type'),
                        youga_houga=request.POST.getunicode('youga_houga'),
                        acquisition_type=request.POST.getunicode('acquisition_type'),
                        title=request.POST.getunicode('title'),
                        target=target,
                        status=status)
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
        else:
            chrome_type = None

        acquisition_type = request.POST.getunicode('acquisition_type')
        if acquisition_type == 'None':
            acquisition_type = None

        target = request.POST.getunicode('status')
        if target == 'target':
            target = 1
            watch_date = None
        elif target == 'unwatched':
            target = 0
            watch_date = None
        elif target == 'watched':
            target = 0
            watch_date = datetime.datetime.today().strftime('%Y-%m-%d')

        movielistdb.update(
            id=request.POST.getunicode('id'),
            release_year=request.POST.getunicode('release_year'),
            youga_houga=youga_houga,
            chrome_type=chrome_type,
            acquisition_type=request.POST.getunicode('acquisition_type'),
            watch_date=watch_date,
            title=request.POST.getunicode('title'),
            target=target)
        return template('edittitle2.html',
                        id=request.POST.getunicode('id'),
                        release_year=request.POST.getunicode('release_year'),
                        youga_houga=youga_houga,
                        chrome_type=chrome_type,
                        acquisition_type=request.POST.getunicode('acquisition_type'),
                        watch_date=watch_date,
                        title=request.POST.getunicode('title'),
                        target=target)
    except Exception as e:
        return str(e)

@route('/scatter')
def scatter():
    return template('scatter.html', scatter=movielistdb.scatter())

@route('/annual_graph_all')
def annual_graph_all():
    try:
        years = movielistdb.read_watched_title()
        year_labels, sum, year_count = movielistdb.get_annual_count(years,
                                                                    lambda title: '年ごと鑑賞数')
        return template('histgram.html',
                        x_labels=year_labels,
                        count=year_count,
                        title='年ごと鑑賞数',
                        sum=sum)
    except Exception as e:
        return str(e)

@route('/annual_graph_by_category')
def annual_graph_by_category():
    years = movielistdb.read_watched_title()
    year_labels, sum, year_count = movielistdb.get_annual_count(years,
                                                                lambda title: title['youga_houga'])
    return template('histgram.html',
                    x_labels=year_labels,
                    count=year_count,
                    title='洋画／邦画区別',
                    sum=sum)

@route('/annual_graph_by_acquisition_type')
def annual_graph_by_acquisition_type():
    years = movielistdb.read_watched_title()
    year_labels, sum, year_count = \
        movielistdb.get_annual_count(years,
                                     lambda title: title['acquisition_type'])
    return template('histgram.html', x_labels=year_labels, count=year_count, title='鑑賞方法', sum=sum)

@route('/annual_graph_by_chrome_type')
def annual_graph_by_chrome_type():
    years = movielistdb.read_watched_title()
    year_labels, sum, year_count = \
        movielistdb.get_annual_count(years,
                                     lambda title: title['chrome_type'])
    return template('histgram.html',
                    x_labels=year_labels,
                    count=year_count,
                    title='カラー／モノクロ区別',
                    sum=sum)

@route('/monthly_graph_all')
def monthly_graph_all():
    years = movielistdb.read_watched_title()
    month_labels, sum, monthly_count = \
        movielistdb.get_monthly_count(years, lambda title: '月ごと鑑賞数')
    return template('histgram.html',
                    x_labels=month_labels,
                    count=monthly_count,
                    title='月ごと鑑賞数',
                    sum=sum)

@route('/monthly_graph_by_category')
def monthly_graph_by_category():
    years = movielistdb.read_watched_title()
    month_labels, sum, monthly_count = \
        movielistdb.get_monthly_count(years, lambda title: title['youga_houga'])
    return template('histgram.html',
                    x_labels=month_labels,
                    count=monthly_count,
                    title='洋画／邦画区別',
                    sum=sum)

@route('/monthly_graph_by_acquisition_type')
def monthly_graph_by_acquisition_type():
    years = movielistdb.read_watched_title()
    month_labels, sum, monthly_count = \
        movielistdb.get_monthly_count(years, lambda title: title['acquisition_type'])
    return template('histgram.html',
                    x_labels=month_labels,
                    count=monthly_count,
                    title='鑑賞方法',
                    sum=sum)

@route('/monthly_graph_by_chrome_type')
def monthly_graph_by_chrome_type():
    years = movielistdb.read_watched_title()
    month_labels, sum, monthly_count = \
        movielistdb.get_monthly_count(years, lambda title: title['chrome_type'])
    return template('histgram.html',
                    x_labels=month_labels,
                    count=monthly_count,
                    title='カラー／モノクロ区別',
                    sum=sum)
