import os
from os import listdir
import numpy as np
import time

# Dir_path = '/Users/chengho/IRterm/txt'
Dir_path = 'data_txt'
word_threshold = 80


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def Load_txt(Dir_path):
    
    files = []
    allData = {}
    
    print('get txt files...', end='\t')
    for i, txtFile in enumerate(listdir_nohidden(Dir_path)):
        path = Dir_path + '/' +  txtFile
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
        f.close()
        name = txtFile.replace('.txt', '')
        allData[name] = data
    N = len(allData)
    print("N= ", N, end='\n')

    ### sort name
    sortedDic = sorted(allData.items(), key=lambda d: d[0]) 

    wordCounts = []
    totalWordCount = {}
    index = 0

    print('build all data')
    for file in sortedDic:
        wordCount = {}
        for w in file[1]:
            if w not in wordCount.keys():
                wordCount[w] = 1
            else:
                wordCount[w] += 1
            if w not in totalWordCount.keys():
                totalWordCount[w] = 1
            else:
                totalWordCount[w] += 1
        wordCounts.append(wordCount)
        index += 1
    
    print("choose word whose count is > " +  str(word_threshold) + '...', end='\t')
    chosenWord = []
    for key, value in totalWordCount.items():
        if value > word_threshold:
            chosenWord.append(key)

    M = len(chosenWord)
    print("M= ", M, end='\n')

    print("build wordCount...")
    X = np.zeros([N, M])
    for w in chosenWord:
        j = chosenWord.index(w)
        for i in range(N):
            if w in wordCounts[i]:
                X[i, j] = wordCounts[i][w]

    return N, M, X, chosenWord, sortedDic

def initializeParameters(lamda, theta):
    print("initialize parameter...")

    lambaRowSum = lamda.sum(axis=1)
    new_lamda = lamda / lambaRowSum[:, np.newaxis]

    thetaRowSum = theta.sum(axis=1)
    new_theta = theta / thetaRowSum[:, np.newaxis]

    return new_lamda, new_theta


def EStep(theta, lamda, p):
    for i in range(N):
        p[i, :, :] = theta.transpose() * lamda[i, :]
        for j in range(M):
            s = p[i, j, :].sum()
            if s == 0:
                p[i, j, :] = np.ones(K)
        row_sum = p[i, :, :].sum(axis=1)
        p[i, :, :] = p[i, :, :] / row_sum[:, np.newaxis]

    return p


def MStep(theta, lamda, p, X):
    for k in range(K):
        for j in range(M):
            theta[k, j] = np.dot(X[:, j], p[:, j, k])
        s = theta[k, :].sum()
        if s == 0:
            theta[k, :] = np.ones(M)
    row_sum = theta.sum(axis=1)
    theta = theta / row_sum[:, np.newaxis]
    for i in range(N):
        for k in range(K):
            lamda[i, k] = np.dot(X[i, :], p[i, :, k])
        s = lamda[i, :].sum()
        if s == 0:
            lamda[i, :] = np.ones(K)
    row_sum = lamda.sum(axis=1)
    lamda = lamda / row_sum[:, np.newaxis]

    return theta, lamda


# calculate the log likelihood
def LogLikelihood(theta, lamda, X):
    loglikelihood = 0
    for i in range(N):
        for j in range(M):
            s = np.dot(theta[:, j], lamda[i, :])
            if s > 0:
                loglikelihood += X[i, j] * np.log(s)

    return loglikelihood

def output():
    ### save files
    np.save('plsa/K=100,threshold=80,final/theta.npy', theta)
    np.save('plsa/K=100,threshold=80,final/lamda.npy', lamda)
    np.save('plsa/K=100,threshold=80,final/X.npy', X)

    # sorted name
    with open('plsa/K=100,threshold=80,final/sortedDic', 'w', encoding='utf-8') as file:
        tmp = ""
        for i in range(len(sortedDic)):
            tmp += sortedDic[i][0] + ', '
            for w in sortedDic[i][1]:
                tmp += w + ' '
            tmp += '\n'
        file.write(tmp)
        file.close()

    # chosen words
    with open('plsa/K=100,threshold=80,final/chosenWord.txt', 'w', encoding='utf-8') as file:
        for i in range(len(chosenWord)):
            file.write(chosenWord[i] + '\n')
        file.close()

    # top words of each topic
    with open('plsa/K=100,threshold=80,final/topicWord.txt', 'w', encoding='utf-8') as file:
        for i in range(0, K):
            # group_score = np.zeros([len(WordsInGroup)])
            topicword = []
            ids = theta[i, :].argsort()
            for j in ids:
                # topicword.insert(0, id2word[j])
                topicword.insert(0, chosenWord[j])
            tmp = ''
            tmp_list = topicword[0:min(50, len(topicword))]
            for word in tmp_list:
                tmp += word + ' '
            file.write(tmp + '\n')
    file.close()


def main():
    
    global N, M, K, X, chosenWord, sortedDic, theta, lamda, p, WordsInGroup
    
    K = 100
    N, M, X, chosenWord, sortedDic = Load_txt(Dir_path)

    lamda = np.random.rand(N, K)  # lamda[i, k] : p(zk|di)
    theta = np.random.rand(K, M)  # theta[k, j] : p(wj|zk)
    p = np.zeros([N, M, K])  # p[i, j, k] : p(zk|di,wj)

    lamda, theta = initializeParameters(lamda, theta)

    iteration = 100
    for i in range(iteration):
        p = EStep(theta, lamda, p)
        theta, lamda = MStep(theta, lamda, p, X)
        loglikelihood = LogLikelihood(theta, lamda, X)
        
        print("[", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "] ", i + 1, " iteration  ",
              str(loglikelihood))


    WordsInGroup = ['運動', '美食', '旅遊', '性感', '文青', '穿搭', '工作', '動物', '其他']

    output()


if __name__ == '__main__':
    main()