import numpy as np
from gensim.models import word2vec

Dir_path = '../data'
# Dir_path = 'final'

def readData():
	### load all word count
	allWordCount = np.load( Dir_path + '/' + 'allWordCount1.npy')

	### load all word list
	with open (Dir_path + '/' + 'allWordList1.txt', encoding='utf-8') as f:
		allWordList = f.read().splitlines()
	f.close()

	### load user and their word
	userID = []
	userWord = []
	allWordSet = set()
	with open(Dir_path + '/' + 'sortedDic', encoding='utf-8') as f:
		lines = f.read().splitlines()
		for line in lines:
			line = line.split(',')	
			userID.append(line[0])
			userWord.append(line[1].split())
			for w in line[1].split():
				allWordSet.add(w)
	f.close()

	# print('save all word list')
	# allWordList = list(allWordSet)
	# with open(Dir_path + '/' + 'allWordList.txt', 'w', encoding='utf-8') as f:
	# 	for w in allWordList:
	# 		f.write(w + '\n')
	# f.close()
	# print(len(allWordList))

	### load chosen word
	# with open(Dir_path + '/' + 'chosenWord.txt', encoding='utf-8') as f:
	# 	chosenWord = f.read().splitlines()

	### load topic word
	# topicList = []
	# with open(Dir_path + '/' + 'topicWord.txt', encoding='utf-8') as f:
	# 	lines = f.read().splitlines()
	# 	for line in lines:
	# 		topicList.append(line.split())
	
	### build word dictionary
	# wordDic = {}
	# for i, topic in enumerate(topicList):
	# 	for j, word in enumerate(topic):
	# 		if word not in wordDic.keys():
	# 			wordDic[word] = [i, j]
	# 		else:
	# 			if wordDic[word][1] > j:
	# 				wordDic[word] = [i, j]

	### all word count
	# allWordCount = np.zeros([len(userID), len(allWordList)])
	# for i, wordList in enumerate(userWord):
	# 	for word in wordList:
	# 		j = allWordList.index(word)
	# 		allWordCount[i, j] += 1
	# np.save('allWordCount.npy', allWordCount)

	return allWordCount, allWordList, userID, userWord

def returnList_org(query):

	### check chosenWord
	# find query id
	if query not in allWordList:
		returnList = 'Sorry, not found'
	else:
		queryID = allWordList.index(query)
		targetList = allWordCount[:, queryID]
		
		indexList = (-targetList).argsort()
		returnList = []
		for i in range(20):
			if(targetList [indexList[i]] > 0):
				returnList.append(userID[indexList[i]])
				# print(userID[indexList[i]],targetList [indexList[i]])
			else:
				break

	return returnList
def returnList(query):
    ### check chosenWord
    # find query id
    model = word2vec.Word2Vec.load(Dir_path + '/' + '/200_10.model.bin')
    if query not in model.wv.vocab:
        returnList = 'Sorry, not found'
    else:
        wordList = [(query,2)]
        wordList.extend(model.most_similar(query))
        score = np.zeros(len(userID))

        queryIDList = []

        for word in wordList:
            print (word)
            wordID = allWordList.index(word[0])
            queryIDList.append(wordID)

        for i, wordID in enumerate(queryIDList):
            weight = wordList[i][1]
            # weight = 11 - i
            # print (weight)
            score = score + np.array(allWordCount[:, wordID]) * weight

        # targetList = allWordCount[:, queryID]
        # indexList = (-targetList).argsort()

        indexList = (-score).argsort()
        returnList = []
        for i in range(20):
            if score[indexList[i]] > 0:
                returnList.append(userID[indexList[i]])
                # print(userID[indexList[i]],score[indexList[i]])
            else:
                break

    return returnList

def main():
	global allWordCount, allWordList, userID, userWord
	print('reading datas...')
	allWordCount, allWordList, userID, userWord = readData()

	### assume query is a single word
	# print('Please type your query')
	# query = input()
	# ans = returnList(query)
	# ans = returnList_org(query)
	# print(ans)
	# return ans
	# a = [1, 3, 5, 7]
	# print(a.index(6))


# if __name__ == '__main__':
# 	main()