import urllib.request
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_all_title(year, month):
    lines = []
    url = 'http://www2.gol.com/users/ip0601170243/private/data/movie/{year}/titlelist_{year}{month:02}.txt'
    req = urllib.request.Request(url.format(year=year, month=month))
    with urllib.request.urlopen(req) as res:
        body = res.read().decode('shift_jis')
        for line in body.split('\n'):
            fields = line.strip().split('\t')
            if len(fields) == 3:
                lines.append(fields[2])
            elif len(fields) == 6:
                lines.append(fields[5])

    return lines


if __name__ == '__main__':
    all_insert_titles = []
    titles2 = None
    for year in range(2015, 2019 + 1):
        for month in range(1, 12 + 1):
            try:
                titles = get_all_title(year, month)
                # print(year, month, len(titles), len(titles2) if titles2 else 0)
                for title in titles:
                    if titles2 is not None and title not in titles2:
                        sql = "update mv_title set insert_date='{}-{:02}-01' where title='{}';"
                        if title not in all_insert_titles:
                            print(sql.format(year, month, title))
                        else:
                            print('-- ' + sql.format(year, month, title))
                        all_insert_titles.append(title)
                titles2 = titles
            except urllib.error.HTTPError:
                pass
