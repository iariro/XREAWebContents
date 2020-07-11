from statistics import mean
from bottle import route, template, request
import ondotoridata

@route('/')
def index():
    ''' ログインページ '''
    return template('login.html')

@route('/devicelist', method="POST")
def devicelist():
    ''' デバイスリスト '''
    try:
        login_id = request.POST.getunicode('login_id')
        login_pass = request.POST.getunicode('login_pass')
        devices = ondotoridata.getCurrentDataFromWebStorage(login_id, login_pass)
        image_url = 'https://ondotori.webstorage.jp/img/device/tr7.svg'
        return template('devicelist.html',
                        login_id=login_id,
                        login_pass=login_pass,
                        image_url=image_url,
                        devices=devices)
    except Exception as e:
        return str(e)

@route('/graph_latest', method="POST")
def graph_latest():
    ''' 最新データグラフ '''
    try:
        login_id = request.POST.getunicode('login_id')
        login_pass = request.POST.getunicode('login_pass')
        remote_serial = request.POST.getunicode('remote_serial')

        daily = ondotoridata.getLatestDataFromWebStorage(login_id, login_pass, remote_serial)
        data_hours = ondotoridata.getDaysSeries(daily)
        data_mean = ondotoridata.getProcessedDaySeries(daily, mean)
        data_max = ondotoridata.getProcessedDaySeries(daily, max)
        data_min = ondotoridata.getProcessedDaySeries(daily, min)

        return template('graph_latest.html',
                        data_hours=data_hours,
                        data_mean=data_mean,
                        data_max=data_max,
                        data_min=data_min)

    except Exception as e:
        return str(e)

@route('/graph_all', method=["POST"])
def graph_all():
    ''' 長期データグラフ '''
    try:
        login_id = request.POST.getunicode('login_id')
        login_pass = request.POST.getunicode('login_pass')
        remote_serial = request.POST.getunicode('remote_serial')
        (monthly, weekly, daily) = ondotoridata.getAllDataFromWebStorage(login_id,
                                                                         login_pass,
                                                                         remote_serial)
        weekly = ondotoridata.getProcessedDaySeries(weekly, mean)
        monthly = ondotoridata.getProcessedDaySeries(monthly, mean)
        annual = ondotoridata.getMeanOfDaySeriesPerYear(daily, start_date='2019/07/01', mean_range=9)

        return template('graph_all.html', weekly=weekly, monthly=monthly, annual=annual)
    except Exception as e:
        return str(e)
