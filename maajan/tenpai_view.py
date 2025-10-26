#!/usr/local/bin/python3
from bottle import route, template, request, run, view, static_file, url, debug
debug(True)

import sys
sys.path.append("../../../python/")

from maajanlib.logic.Pai import Pai
from maajanlib.logic.PaiKind import PaiKind, PaiKindShort
from maajanlib.logic.MachiPattern import MachiPattern
from maajanlib.logic.Chiniso import generate_chiniso_tenpai

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

def tenpai_core(tehai):
    tehai_img = [get_image_file_name(p.kind) for p in tehai]

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

@route('/tenpai', method='POST')
def tenpai():
    tehai_line = request.POST.getunicode('tehai')
    tehai = [Pai(PaiKindShort.value_of(p)) for p in tehai_line.split()]
    return tenpai_core(tehai)

@route('/tenpai2', method='POST')
def tenpai2():
    tehai_line = request.POST.getunicode('tehai2')
    start, line = tehai_line.split(':')
    tehai = []
    for i, n in enumerate(line):
        for j in range(0, int(n)):
            tehai.append(Pai(PaiKindShort.value_of('{}{}'.format(start[0], int(start[1]) + i))))
    return tenpai_core(tehai)

@route('/tenpai3', method='POST')
def tenpai3():
    tehai, line, machiPattern = generate_chiniso_tenpai()
    return tenpai_core(tehai)
