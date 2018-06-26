import query
import sys

'''
如何使用query.py
Prepare: 將query.py放在./下
Work:
import query
input_dataset = Database的路徑 (e.g. ./output_new_policy3.txt) [Type: txt]
prefer_score = user-prefer的分數 (老蕭前端) [Type: dic]
query_list = Text model產出的結果 (振合&阿岳) [Type: list]

1. call query.buildDataBase(input_dataset) 來連結Database
    return userList[Type: list], Database[Type: list]
2. call query.comparePreAndQry(prefer_score, query_list, userList, Database) 來比對user_prefer與text model的結果，並由關聯度大到小排序
    return query_list[Type: list]
'''


# Link pre-trained database
userList, Database = query.buildDataBase(sys.argv[1])  # output_new_policy3.txt

# from 選照片
prefer_score = {'animal': 2, 'exercise': 141, 'food': 5, 'hipster': 65,
                'outfit': 40, 'sexy': 116, 'travel': 1, 'work': 44, 'other': 17}

# Query from 振合&阿岳
query_list = ['imstephaniekuo', 'imtwiggy',
              'jasschatz', 'kaiyibai', 'yin.i_']

# print('query list = ', query_list)
query_list = query.comparePreAndQry(
    prefer_score, query_list, userList, Database)


print('query_list = ', query_list)
