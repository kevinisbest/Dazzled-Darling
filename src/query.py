import sys
import pickle
import numpy as np
from scipy import spatial
import ast

class_list = ['animal', 'exercise', 'food', 'hipster',
              'outfit', 'sexy', 'travel', 'work', 'other']


def getUsrPrefer(prefer_score):
    score = []
    for c in class_list:
        score.append(prefer_score[c])
    else:
        scoreNorm = [float(i) / sum(score) for i in score]
    return scoreNorm


def getScore(user, userList, Database):
    index = userList.index(user)
    score = []
    for c in class_list:
        score.append(Database[index][c])
    scoreNorm = [float(i) / sum(score) for i in score]
    return scoreNorm


def getNewQuery(prefer_score, query_list, userList, Database):
    query_scores = []
    for query in query_list:
        query_scores.append(getScore(query, userList, Database))

    cos_score = []
    for query_score in query_scores:
        cos_score.append(
            1 - spatial.distance.cosine(prefer_score, query_score))

    cos_score, query_list = zip(
        *sorted(zip(cos_score, query_list), reverse=True))

    return list(query_list)


def buildDataBase(input_file):
    count = 0
    stat = []
    DataBase = []
    userList = []
    with open(input_file) as f:
        for line in f:
            if count % 2 != 0:  # Dict
                d = ast.literal_eval(line)
                DataBase.append(d.copy())
                max_value = max(d.values())  # maximum value
                # getting all keys containing the `maximum`
                max_keys = [k for k, v in d.items() if v == max_value][0]
                stat.append(list(d.keys()).index(max_keys))
            else:  # userList
                userList.append(line.split(' ')[0])
            count += 1
    return userList, DataBase


def check(prefer_score):
    flag = True
    score = []
    for c in class_list:
        score.append(prefer_score[c])
    if sum(score) == 0:
        flag = False
    return flag


def comparePreAndQry(prefer_score, query_list, userList, Database):
    if check(prefer_score):
        prefer_score = getUsrPrefer(prefer_score)
        query_list = getNewQuery(prefer_score, query_list, userList, Database)
    else:
        return query_list
    return query_list


if __name__ == '__main__':

    # Link pre-trained database
    userList, Database = buildDataBase(sys.argv[1])  # output_new_policy3.txt

    # from 選照片
    prefer_score = {'animal': 2, 'exercise': 141, 'food': 5, 'hipster': 65,
                    'outfit': 40, 'sexy': 116, 'travel': 1, 'work': 44, 'other': 17}
    # prefer_score = {'animal': 0, 'exercise': 0, 'food': 0, 'hipster': 0,
    #                 'outfit': 0, 'sexy': 0, 'travel': 0, 'work': 0, 'other': 0}

    # Query from 振合&阿岳
    query_list = ['imstephaniekuo', 'imtwiggy',
                  'jasschatz', 'kaiyibai', 'yin.i_']

    # print('query list = ', query_list)
    query_list = comparePreAndQry(prefer_score, query_list, userList, Database)
    # print('query list = ', query_list)
