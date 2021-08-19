from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from tempfile import TemporaryFile
import os
import pickle
import random
import operator
import math
import numpy as np
from scipy.stats._multivariate import matrix_normal_frozen

from musicGenreTest import *

def getAccuracy(testSet, predictions):
    correct = 0
    for x in range (len(testSet)):
        if testSet[x][-1]==predictions[x]:
            correct+=1
    return 1.0*correct/len(testSet)

directory = "C:/Users/Korisnik/Desktop/faks/musicDataSet/genres/"
f= open("my.dat" ,'wb')
i=0

for folder in os.listdir(directory):
    i+=1
    print(directory, folder)
    if i==8 :
        break
    for file in os.listdir(directory+folder):
        print(directory, folder, file)
        (rate, sig) = wav.read(directory+folder+"/"+file)
        mfcc_feat = mfcc(sig, rate, nfft=960, winlen=0.020, appendEnergy=False)
        #print(mfcc_feat, " mfcc_feat")
        covariance = np.cov(np.matrix.transpose(mfcc_feat))
        mean_matrix = mfcc_feat.mean(0)
        #print(mean_matrix, " mean_matrix")
        feature = (mean_matrix, covariance, i)
        pickle.dump(feature, f)

f.close()

dataset = []
def loadDataset(filename , split , trSet , teSet):
    with open("my.dat" , 'rb') as f:
        while True:
            try:
                dataset.append(pickle.load(f))
            except EOFError:
                f.close()
                break

    for x in range(len(dataset)):
        if random.random() <split :
            trSet.append(dataset[x])
        else:
            teSet.append(dataset[x])

trainingSet = []
testSet = []
loadDataset("my.dat" , 0.66, trainingSet, testSet)


leng = len(testSet)
predictions = []
for x in range (leng):
    predictions.append(nearestClass(getNeighbors(trainingSet ,testSet[x] , 5)))

accuracy1 = getAccuracy(testSet , predictions)
print(accuracy1)




