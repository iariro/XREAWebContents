#!/usr/local/bin/python3
from bottle import route, template, request, run, view, static_file, url

import sys
sys.path.append("../../../python/")

from maajanlib.logic.Pai import Pai
from maajanlib.logic.PaiKind import PaiKind, PaiKindShort
from maajanlib.logic.MachiPattern import MachiPattern

pai_image_list = []
pai_image_list += ['man_{}.png'.format(i) for i in range(1, 10)]
pai_image_list += ['pin_{}.png'.format(i) for i in range(1, 10)]
pai_image_list += ['sou_{}.png'.format(i) for i in range(1, 10)]
pai_image_list += ['kaze_ton.png', 'kaze_nan.png', 'kaze_sha.png', 'kaze_pei.png',
                   'sangen_haku.png', 'sangen_hatu.png', 'sangen_chun.png',]

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
        tehai_img = [pai_image_list[PaiKindShort.value_of(p)] for p in tehai_line.split()]

        machiPattern = MachiPattern(tehai, True)
        machi_detail = []
        for element in machiPattern.machiElementCollection.sort():
            machi_detail.append({'type': element.type_jp.name, 'pai_list': [pai_image_list[m] for m in element.pai_list]})
        machi = machiPattern.getMachi()
        machi_img = [pai_image_list[m] for m in machi]

        return template('tenpai.html', tehai=tehai_img, machi=machi_img, machi_detail=machi_detail)
    except Exception as e:
        return str(e)
