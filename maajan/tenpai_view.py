#!/usr/local/bin/python3
from bottle import route, template, request, run, view, static_file, url

import sys
sys.path.append("../../../python/")

from maajanlib.logic.Pai import Pai
from maajanlib.logic.PaiKind import PaiKind, PaiKindShort
from maajanlib.logic.MachiPattern import MachiPattern

pai_image_list = []
pai_image_list += ['man_{}'.format(i) for i in range(1, 10)]
pai_image_list += ['pin_{}'.format(i) for i in range(1, 10)]
pai_image_list += ['sou_{}'.format(i) for i in range(1, 10)]
pai_image_list += ['kaze_ton', 'kaze_nan', 'kaze_sha', 'kaze_pei',
                   'sangen_haku', 'sangen_hatu', 'sangen_chun',]

def get_image_file_name(m, valid=True):
    return pai_image_list[m]+ ('_gray' if valid == False else '') + '.png'

@route('/image/<filepath:path>', name='static_file')
def static(filepath):
    return static_file(filepath, root="./views/image")

@route('/')
def index():
    return template('index.html')

@route('/tenpai', method='POST')
def tenpai():
    try:
        tehai_line = request.POST.getunicode('tehai')
        tehai = [Pai(PaiKindShort.value_of(p)) for p in tehai_line.split()]
        tehai_img = [get_image_file_name(PaiKindShort.value_of(p)) for p in tehai_line.split()]

        machiPattern = MachiPattern(tehai, True)
        machi_detail = []
        for i, element in enumerate(machiPattern.machiElementCollection.sort()):
            pai_list = []
            for j, m in enumerate(element.pai_list):
                if j == 0:
                    valid = element.over1 == False
                elif j == 1:
                    valid = element.over2 == False
                pai_list.append(get_image_file_name(m, valid=valid))
            machi_detail.append({'type': element.type_jp.name, 'pai_list': pai_list})
        machi = machiPattern.getMachi()
        machi_img = [get_image_file_name(m) for m in machi]

        return template('tenpai.html', tehai=tehai_img, machi=machi_img, machi_detail=machi_detail)
    except Exception as e:
        return str(e)
