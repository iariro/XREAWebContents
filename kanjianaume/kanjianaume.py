import json
import os
import random
 
def read_word():
    with open('2charwordlist.txt') as file:
        return [line.strip() for line in file]
 
def read_valid_chars():
    with open('validchars.txt') as file:
        return [line.strip() for line in file]

def delete_invalid_word(word_list):
    word_list2 = []
    for word in word_list:
        if word[0] == word[1]:
            continue
        if len([word for ch in ['々', 'α', 'β', 'δ', 'θ', 'μ', '～', '-', '°', '2'] if ch in word]) > 0:
            continue
        if word[0] in ('一', '二', '三', '四', '五' , '六', '七', '八', '九'):
            if word[1] in ('十', '百', '月', '日', '塁', '度', '分'):
                continue
        word_list2.append(word)

    return word_list2

def check_numeric_word(word_list):
    ch2 = {}
    for word in word_list:
        if word[0] in ('二', '三', '四', '五' , '六', '七', '八', '九', '十', '百'):
            if word[1] not in ch2:
                ch2[word[1]] = []
            ch2[word[1]].append(word[0])

    for c, ch1 in ch2.items():
        print(ch1, c)

def get_hist_data(word_list):
    char1 = set([word[0] for word in word_list])
    char2 = set([word[1] for word in word_list])
    char12and = char1 & char2
    char12or = char1 | char2

    count_list = {}
    for c in char12and:
        count_list[c] = [0, 0]
        for i in (0, 1):
            count_list[c][i] = len([word for word in word_list if word[i] == c])
    return count_list, len(char12or)

def check_link_count(word_list, count_list):
    valid_chars = []
    count_rank = []
    for c, counts in sorted(count_list.items(), key=lambda x: x[1][0] + x[1][1]):
        qword = [[], []]
        for word in word_list:
            if word[0] == c:
                qword[0].append(word)
            if word[1] == c:
                qword[1].append(word)
        if len(qword[0]) >= 2 and len(qword[1]) >= 2:
            valid_chars.append(c)
        count_rank.append(counts[0] + counts[1])

    return valid_chars, count_rank

def make_question(word_list, valid_chars):
    c = random.choice(valid_chars)
    qword = [[], []]
    for word in word_list:
        if word[0] == c:
            qword[0].append(word)
        if word[1] == c:
            qword[1].append(word)
    if len(qword[0]) < 2 or len(qword[1]) < 2:
        return None, None, None
    qc1 = random.sample(qword[0], 2)
    qc2 = random.sample(qword[1], 2)
    if qc2[0][0] == qc1[1][1] or qc2[1][0] == qc1[0][1]:
        return None, None, None
    return qword, qc1, qc2

def solve(word_list, qc1, qc2):
    word1 = [word[0] for word in word_list if qc1[0][1] == word[1]]
    word2 = [word[0] for word in word_list if qc1[1][1] == word[1]]
    word3 = [word[1] for word in word_list if qc2[0][0] == word[0]]
    word4 = [word[1] for word in word_list if qc2[1][0] == word[0]]
    return list(set(word1) & set(word2) & set(word3) & set(word4))
