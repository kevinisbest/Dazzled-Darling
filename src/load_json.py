import json
import os
from os import listdir
from os.path import isfile, join
import codecs
import jieba
import re

# dir path
# Dir_path = '/Users/kevin_mbp/Desktop/IG/test_users'
Dir_path = '/Users/chengho/IRterm'


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def Load_json(dir_path):
    usernames = []
    stopWords = []
    IdDict = {}
    TagDict = {}
    ContentDict = {}

    with open('stopword.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)
    # print(stopWords)
    file.close() 

    # puncs = [u'?', u'\n', u'⋯', u'·', u'\'', u'\"', u'，', u'@', u'$', u'&', u':', u'#',u'!', u'～', u'$', u'%', u'『', u'』', u'「', u'」', u'＼', u'/', u'｜', u'？', u' ', u'*', u'(', u')', u'~', u'.', u'[', u']', 'u\n',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0', u'。',u'-']
    # emoji_pattern = re.compile("["
    #     ## UCS-4
    #     u"\U0001F600-\U0001F64F"  # emoticons
    #     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #     u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    #     u"\U00002600-\U000027BF"
    #     u"\U0001F900-\U0001F9FF"

    #     ## UCS-2
    #     u"\u200D"
    #     u"\u2600-\u27BF"
    #     u"\uD83C"
    #     u"\uDF00-\uDFFF"
    #     u"\uD83D"
    #     u"\uDC00-\uDE4F"
    #     u"\uDE80-\uDEFF"

    #     "]+", flags=re.UNICODE)

    # chinese_pattern = re.compile("["
    #     u"\uac00-\ud7ff"
    #     "]+", flags=re.UNICODE)


    for i, username in enumerate(listdir_nohidden(dir_path)):
        usernames.append(username)
        json_file = listdir(join(dir_path,username))
        f = codecs.open(join(dir_path,username,json_file[0]), 'r', 'utf-8')
        data = json.load(f)
        IdDict[username] = data[0]['owner']['id']
        for j in range(len(data)):
            ### tags ###
            tags = data[j]['tags']
            for tag in tags :
                tag = tag.lower().strip()
                segments = jieba.cut(tag,cut_all=False)
                tag = list(filter(lambda a: a not in stopWords and a != '\n', segments))
                try:
                    TagDict[username]
                except :
                    TagDict[username] = tag
                else:
                    TagDict[username] = TagDict[username] + tag

            ### contents ###
            contents = data[j]['edge_media_to_caption']['edges'][0]['node']['text']

            res = re.findall(u"[\u4e00-\u9fa5]+", contents)
            # for punc in puncs:
            #     contents = contents.replace(punc,'')
            # print(contents)
            # print(type(contents))
            # contents = contents.lower().strip()
            # contents = emoji_pattern.sub(r'', contents)
            contents = ""
            for word in res:
                contents += word
            segments = jieba.cut(contents,cut_all=False)

            # # print(contents)
            content = list(filter(lambda a: a not in stopWords 
                                    and a != '\n'
                                    ##and a.encode('utf8')!= b'\xef\xb8\x8f'
                                    , segments))
            try:
                ContentDict[username]
            except:
                ContentDict[username] = content
            else:
                ContentDict[username] = ContentDict[username] + content

    # print(TagDict)
    print(ContentDict)

def main():
    Load_json(Dir_path)

if __name__ == '__main__':
    main()
