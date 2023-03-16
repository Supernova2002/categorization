import numpy as np
import nltk
from nltk.corpus import stopwords
def calc_sim(catVec, docVec):
    dotProd  = np.dot(catVec, docVec)
    catSum = 0
    for value in catVec:
        catSum = catSum + np.power(value, 2)
    docSum = 0
    for value in docVec:
        docSum = docSum + np.power(value,2)  
    sim = dotProd/(catSum*docSum)
    return sim
    

sentence = """At eight o'clock on Thursday morning  Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
categories = []
catFreq = []
stopWords = set(stopwords.words('english'))
wordBank = []
docsContaining = []
totalFiles = 0
#print(stopwords.words('english'))
#trainingFile = input("Input relative location of training file:\n")
trainingFile = "./TC_provided/corpus1_train.labels"
testingFile = "./TC_provided/corpus1_test.list"
#testingFile = input("Input relative location of testing file name:\n")
trainingDocs = open(trainingFile,'r')
for line in trainingDocs:
    totalFiles = totalFiles + 1
    currentLine = line
    words = currentLine.split(' ')
    #fileLoc = words[0]
    fileLoc = "./TC_provided" + words[0][1:]
    fileType = words[1].split('\n')[0]
    #print(totalFiles)
    if fileType not in categories:
        #print(fileType)
        categories.append(fileType)
        catFreq.append(1)
    else:
        catFreq[categories.index(fileType)] = catFreq[categories.index(fileType)] + 1
    article = open(fileLoc,'r') 
    Lines = article.readlines()
    
    #wordsChecked = []
    for subLine in Lines:
        #print(line)
        tokenizedLine = nltk.word_tokenize(subLine)
        for word in tokenizedLine:
            if word.lower() not in stopWords:
                if word.lower() not in wordBank:
                    wordBank.append(word.lower())
                    #docsContaining.append(1)
                
                        


        #print(tokenizedLine)
#Now that I have all the words in the corpus and the categories, I can define matrices of rigid shape without needing to dynamically add on to them
wordFreq = np.zeros([len(categories),len(wordBank)]) + 0.5

print("VECTORS MADE")
#print(wordFreq)  
print(catFreq)
print(categories)
#testing
trainingDocs = open(trainingFile,'r')
for line in trainingDocs:
    wordsChecked = []
    currentLine = line
    words = currentLine.split(' ')
    fileLoc = "./TC_provided" + words[0][1:]
    fileType = words[1].split('\n')[0]
    article = open(fileLoc,'r')
    Lines = article.readlines()
    for subLine in Lines:
        tokenizedLine = nltk.word_tokenize(subLine)
        for word in tokenizedLine:
            
            if word.lower() not in stopWords:
                
                if word.lower() not in wordsChecked:
                    wordsChecked.append(word.lower())
                    wordFreq[categories.index(fileType)][wordBank.index(word.lower())] =  wordFreq[categories.index(fileType)][wordBank.index(word.lower())] + 1

#p(t|c) = # doc in c that contain t / # doc in c
testingDocs = open(testingFile,'r')
outputDoc = open(r"testOutput.labels","w")
for line in testingDocs:
    wordsChecked = []
    #simVals = np.zeros([1,len(categories)])
    simVals = []
    docVector = []
    #docVector = np.zeros([1,len(wordBank)])
    fileName = "./TC_provided" + line.split('\n')[0][1:]
    testArticle = open(fileName, 'r')
    testLines = testArticle.readlines()
    for testLine in testLines:
        tokenizedTestLine = nltk.word_tokenize(testLine)
        for word in tokenizedTestLine:
            if word.lower() not in stopWords:
                if word.lower() in wordBank:
                    docVector.append(word.lower())
                    wordsChecked.append(word.lower())
                    #docVector[0][wordBank.index(word.lower())] = docVector[0][wordBank.index(word.lower())] + 1
    for category in categories:

        catIndex = categories.index(category)
        temp = np.log(catFreq[catIndex]/totalFiles)
        length = len(wordFreq[catIndex])
        fcatArray = np.reshape(wordFreq[catIndex],(1,length))
        for word in docVector:
            wordCount = wordFreq[catIndex][wordBank.index(word.lower())]
            #print(wordCount)
            
            #keep getting a divide by zero error here
            if wordCount != 0:
                temp = temp + np.log(wordCount/(catFreq[catIndex]))
            
        
    
        #print(temp)
       # print(np.shape(simVals))
        simVals.append(temp)
    #print(simVals)
    finalIndex = simVals.index(max(simVals))
    #print(categories[finalIndex])
    outputDoc.write(fileName + " " + categories[finalIndex] + "\n")
    #finalSimVals = np.array(simVals)
    #max = np.max(finalSimVals[0])
    #print(max)
    #catIndex = np.where(finalSimVals == max)[0]
    #print(catIndex)
    #print(categories[catIndex[0]])
    #print(categories[simVals.index(max)])
    


    

    



