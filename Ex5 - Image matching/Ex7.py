# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 00:30:05 2021

@author: Christian
"""


import naturalize as nat
import numpy as np
import os
import matplotlib.pyplot as plt
from functions import Environment, ftest, fitness, renderImg, testIndividual

dx = 200
dy = 200
ImageName = 'target_circle.jpg'
OutputData = 'Gen_4000.P'
outputGif = 'generations.gif'
env = Environment(dx,dy,ImageName)

Ncircle = 100
rmax = 10
lims = np.array([dx, dy, rmax, 255])

llims =  [np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle) * 0.]
ulims =  [np.ones(Ncircle)*dx, np.ones(Ncircle)*dy, np.ones(Ncircle)*rmax, np.ones(Ncircle)*255]
genePool = nat.BasicGenePool(llims, ulims)


helper = nat.AlgorithmHelper(ftest, genePool, fitness, environment = env, fmut = nat.getMutate(0))

Ngen = 1000
Npop = 10
Ncouples = 4
Nsurvive = 1
mutateThresold = 0.0001
# mutateThresold = 0.005


algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold)
# recorder = nat.basicRecorder(100, 5)
recorder = nat.basicRecorder(10, 1)
analysis = nat.Analysis(algorithm, recorder,False)

# gen = nat.readPickle('Gen160000_1000.P')
best = analysis.runAnalysis(Ngen)
nat.pickleAnalysis(analysis.currentGen, OutputData)

img = renderImg(*best, dx,dy)

data = analysis.getRecorderData()
nat.pickleAnalysis(data, 'RecordedData.P')

plt.plot(data.genNumber, data.bestScores)

out = renderImg(*best, dx, dy)
# =============================================================================
# 
# =============================================================================


# nat.plotAvgScore(data,1)
nat.plotGeneValue(data, 2, 1)

imgPixel = np.array(img, float)
targetPixel = np.array(env.target)
diff = np.sum((imgPixel - targetPixel)**2)

test = imgPixel - targetPixel

# output = data.bestGenotypes
images = []
for genotype in data.bestGenotypes:
    img = renderImg(*genotype, dx,dy)
    images.append(img)
    
images[0].save(outputGif,
               save_all = True, append_images = images[1:], 
               optimize = False, duration = 2)


