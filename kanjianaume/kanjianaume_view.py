#!/usr/local/bin/python3
from bottle import route, template, request, run, view, static_file, url

import sys
import kanjianaume

@route('/')
def index():
    word_list = kanjianaume.read_word()
    black_list = kanjianaume.read_black_list()
    valid_chars = kanjianaume.read_valid_chars()
    return template('index.html',
                    word_list_count=len(word_list),
                    valid_chars_count=len(valid_chars),
                    black_list_count=len(black_list))

@route('/makequestion', method='POST')
def makequestion():
    try:
        word_list = kanjianaume.read_word()
        black_list = kanjianaume.read_black_list()
        word_list = kanjianaume.delete_invalid_word(word_list, black_list)
        valid_chars = kanjianaume.read_valid_chars()
        qword, qc1, qc2, valid = kanjianaume.make_question(word_list, valid_chars)
        if qword and qc1 and qc2:
            solved_chars = kanjianaume.solve(word_list, qc1, qc2)
            return template('question.html',
                            qword1=' '.join(qword[0]),
                            qword2=' '.join(qword[1]),
                            qc1_qc2=' '.join(qc1 + qc2),
                            chars=[qc2[0][0], qc2[1][0], qc1[0][1], qc1[1][1]],
                            center_char=qc1[0][0],
                            solved_chars=' '.join(solved_chars),
                            valid='valid' if valid else 'invalid')
        else:
            return template('question.html',
                            qword1=' '.join(qword[0]),
                            qword2=' '.join(qword[1]),
                            chars=['-', '-', '-', '-'],
                            center_char=qc1[0][0],
                            solved_chars='-',
                            valid='valid' if valid else 'invalid')
    except Exception as e:
        return str(e)

@route('/blacklist', method='POST')
def blacklist():
    try:
        word_list = request.POST.getunicode('word_list')
        with open('blacklist.txt' ,'a') as blacklist:
            for word in word_list.split():
                blacklist.write('{}\n'.format(word))
        return template('blacklist.html')
    except Exception as e:
        return str(e)
