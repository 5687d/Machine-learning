# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g2Efmg3bJW-MFpF3qjiQGNNbgGZ_tA6U
"""

from google.colab import drive
drive.mount('/content/drive/')

# -*- coding: utf-8 -*-

"""

@author: yh960
reference: https://www.programmersought.com/article/12664496909/
           https://www.kaggle.com/shrutimechlearn/step-by-step-diabetes-classification-knn-detailed
           https://www.w3xue.com/exp/article/20201/73169.html 
"""
import numpy
import csv
import time
import torch

device = torch.device("cuda:0")

# load the train data
def loadTrainData():
     l=[]
     with open('/content/drive/My Drive/lab/train.csv') as file:
          lines = csv.reader(file)
          for line in lines:
              l.append(line)
          l.remove(l[0])
          l=array(l)
          print(l.shape)
          data, label = l[:,1:], l[:,0]
          label = label[:,newaxis]
          data = toInt(data)
          label = toInt(label)
          return data, label

# integer
def toInt(array):
    tensor = torch.from_numpy(array.astype(numpy.int_)).to(device)
    print('toInt: size = ' + str(tensor.size()))
    return tensor
  
# Normalization
#def normalizing(array):
#    m,n = shape(array)
#    for i in range(m):
#        for j in range(n):
#            if array[i,j] != 0:
#                array[i,j]=1
#    return array
  
# load the test data
def loadTestData():
      l=[]         

      with open('/content/drive/My Drive/lab/test.csv') as file:
          lines = csv.reader(file)
          for line in lines:
              l.append(line)
          l.remove(l[0])
          l=array(l)
          testdata=toInt(l)
          return testdata
  
# save the result
def saveResult(result):
      with open('/content/drive/My Drive/lab/knn.csv', 'w', newline='') as myFile:
          myWriter = csv.writer(myFile)
          myWriter.writerow(['ImageId','Label'])
          for i, label in enumerate(result):
              tmp = [i+1, int(label)]
              myWriter.writerow(tmp)

trainData,trainLabel=loadTrainData()
testData =loadTestData()

# kNN classifier
def classify(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = inX.repeat(dataSetSize,1)-dataSet

    # calculate the L2 distance
    spDiffMat = torch.square(diffMat)
    spDistances = torch.sum(spDiffMat,dim=1) 
    distances = spDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}

    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i],0]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=lambda item:item[1], reverse=True)
    return sortedClassCount[0][0]
  
# main
start = time.time()

errorCount=0
resultList=[]
splitTrainDataSize = 33600
splitTestDataSize = 8400
k=1

splitTrainData = torch.split(trainData, [splitTrainDataSize, splitTestDataSize])
splitTrainLabel = torch.split(trainLabel, [splitTrainDataSize, splitTestDataSize])
for i in range(splitTestDataSize):
    classifierResult = classify(splitTrainData[1][i], splitTrainData[0], splitTrainLabel[0], k)
    #resultList.append(classifierResult)
    if i % 1000 == 0:
        print(time.time()-start)
    #print("the classifier for %d came back with: %d, the actual answer is %d" % (i, classifierResult, splitTrainLabel[1][27]))
    if (classifierResult != splitTrainLabel[1][i]): 
        errorCount += 1



end = time.time()
print (end - start)
print("\nthe total number of errors is: %d" % errorCount)
print("\nthe total error rate is: %f" % (errorCount/float(splitTestDataSize)))

start = time.time()
testDataSize = testData.shape
print(testDataSize)
for i in range(testDataSize[0]):
    classifierResult = classify(testData[i], splitTrainData[0], splitTrainLabel[0], k)
    resultList.append(classifierResult)
    if i % 1000 == 0:
        print(time.time()-start)
    #print("the classifier for %d came back with: %d, the actual answer is %d" % (i, classifierResult, splitTrainLabel[1][i]))
    #if (classifierResult != splitTrainLabel[1][i]): 
        #errorCount += 1


saveResult(resultList)