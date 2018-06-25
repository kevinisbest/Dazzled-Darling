import numpy as np

Dir_path = '../data'
# Dir_path = 'final'

def readData():
	### load all word count
	allWordCount = np.load( Dir_path + '/' + 'allWordCount.npy')

	### load all word list
	with open (Dir_path + '/' + 'allWordList.txt', encoding='utf-8') as f:
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
	with open(Dir_path + '/' + 'chosenWord.txt', encoding='utf-8') as f:
		chosenWord = f.read().splitlines()
	f.close()

	### load topic word
	topicList = []
	with open(Dir_path + '/' + 'topicWord.txt', encoding='utf-8') as f:
		lines = f.read().splitlines()
		for line in lines:
			topicList.append(line.split())
	f.close()
	
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

	return allWordCount, allWordList, userID, userWord, chosenWord, topicList

def returnList(query):

	### check chosenWord
	# find query id
	if query not in allWordList:
		returnList = 'Sorry, not found'
	else:
		queryID = allWordList.index(query)

		targetList = allWordCount[:, queryID]
		rankList = (-targetList).argsort()
		returnList = []
		for i in range(20):
			returnList.append(userID[rankList[i]])

	return returnList

def main(query):
	global allWordCount, allWordList, userID, userWord, chosenWord, topicList
	print('reading datas...')
	allWordCount, allWordList, userID, userWord, chosenWord, topicList = readData()

	### assume query is a single word
	# print('Please type your query')
	# query = input()
	ans = returnList(query)
	print(ans)
	return ans
	# a = [1, 3, 5, 7]
	# print(a.index(6))


# if __name__ == '__main__':
# 	main()