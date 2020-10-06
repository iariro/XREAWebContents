#!/usr/local/bin/python3
import datetime
import re
import urllib.request

def getIpmiutilVersion():
    today = datetime.date.today()
    versions = []
    url = 'http://ipmiutil.sourceforge.net/docs/ChangeLog'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read().decode()
        dt2 = None
        for line in body.split('\n'):
            m = re.match(r'(^[0-9]*\/[0-9]*\/[0-9]*) (.*) ipmiutil-([0-9]*.[0-9]*.[0-9]*)', line)
            if m:
                if len(m.group(1)) == 8:
                    dt = datetime.datetime.strptime(m.group(1), '%m/%d/%y').date()
                elif len(m.group(1)) == 10:
                    dt = datetime.datetime.strptime(m.group(1), '%m/%d/%Y').date()
                versions.insert(0, {'date': dt.strftime('%Y/%m/%d'),
                                    'author': m.group(2),
                                    'version': m.group(3),
                                    'diff': (dt - dt2).days if dt2 else 0,
                                    'ago': (today - dt).days})
                dt2 = dt

    return versions


if __name__ == '__main__':
    print(getIpmiutilVersion()[0:10])
