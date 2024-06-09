#!/usr/local/bin/python3
from bottle import route, template, request, run, view, static_file, url

import sys
import kanjianaume

@route('/')
def index():
    word_list = kanjianaume.read_word()
    valid_chars = kanjianaume.read_valid_chars()
    return template('index.html', word_list_count=len(word_list), valid_chars_count=len(valid_chars))

@route('/makequestion', method='POST')
def makequestion():
    try:
        word_list = kanjianaume.read_word()
        valid_chars = kanjianaume.read_valid_chars()
        qword, qc1, qc2 = kanjianaume.make_question(word_list, valid_chars)
        solved_chars = kanjianaume.solve(word_list, qc1, qc2)
        return template('question.html',
                        qword1=' '.join(qword[0]),
                        qword2=' '.join(qword[1]),
                        chars=[qc2[0][0], qc2[1][0], qc1[0][1], qc1[1][1]],
                        center_char=qc1[0][0],
                        solved_chars=' '.join(solved_chars))
    except Exception as e:
        return str(e)
