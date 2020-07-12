from bottle import route, template, request
import datetime
import hardoffdata

@route('/')
def index():
    return template('index.html')

@route('/area_count')
def area_count():
    (prefectures, visited, unvisited) = hardoffdata.get_area_count()
    prefectures = ','.join(["'%s'" % v for v in prefectures])
    visited = ','.join([str(v) for v in visited])
    unvisited = ','.join([str(v) for v in unvisited])
    return template('area_count.html', prefectures=prefectures, visited=visited, unvisited=unvisited)

@route('/completion_history')
def completion_history():
    (bardata, linedata) = hardoffdata.get_completion_history()
    bardata = ','.join([str(v) for v in bardata])
    linedata =','.join( [str(v) for v in linedata])
    return template('completion_history.html', bardata=bardata, linedata=linedata)

@route('/store_edit1', method='POST')
def store_edit1():
    store_id = request.POST.getunicode('store_id')
    name = request.POST.getunicode('name')
    near_station = request.POST.getunicode('near_station')
    minutes_from_near_station = request.POST.getunicode('minutes_from_near_station')
    visit_date = request.POST.getunicode('visit_date')
    address = request.POST.getunicode('address')
    targeting = request.POST.getunicode('targeting')
    return template('store_edit1.html',
                    store_id=store_id,
                    name=name,
                    near_station=near_station,
                    minutes_from_near_station=minutes_from_near_station,
                    visit_date=visit_date,
                    address=address,
                    targeting=targeting)

@route('/store_edit2', method='POST')
def store_edit2():
    store_id = request.POST.getunicode('store_id')
    near_station = request.POST.getunicode('near_station')
    minutes_from_near_station = request.POST.getunicode('minutes_from_near_station')
    visit_date = request.POST.getunicode('visit_date')
    address = request.POST.getunicode('address')
    targeting = request.POST.getunicode('targeting')
    try:
        sql = hardoffdata.update_store(store_id, near_station, minutes_from_near_station, visit_date, address, targeting)
        return template('store_edit2.html', success=True, sql=sql)
    except:
        return template('store_edit2.html', success=False, sql=sql)

@route('/store_list', method='POST')
def store_list():
    where = request.POST.getunicode('where')
    (count, days) = hardoffdata.get_store_list(where)
    return template('store_list.html', count=count, days=days)

@route('/store_visit_today', method='POST')
def store_visit_today():
    store_id = request.POST.getunicode('store_id')
    hardoffdata.update_visit_date(store_id, datetime.date.today())
    return template('store_visit.html')
