# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 00:30:05 2021

@author: Christian
"""


import naturalize as nat
import numpy as np
import os
import dill

import matplotlib.pyplot as plt


from functions import Environment, ftest, fitness, renderImg

dx = 252
dy = 204
ImageName = 'Ex4.2-target.jpg'
inputGen = 'Gen650000_2.P'
outputGen = 'Gen650000_2.P'
outputGen = 'TEST.P'
env = Environment(dx,dy, ImageName)

Ncircle = 1000
rmax = 10
lims = np.array([dx, dy, rmax, 255])

llims =  [np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle), np.zeros(Ncircle) * 0.]
ulims =  [np.ones(Ncircle)*dx, np.ones(Ncircle)*dy, np.ones(Ncircle)*rmax, np.ones(Ncircle)*255]
# fmut = nat.getMutate(1, p = 0.1)


genePool = nat.BasicGenePool(llims, ulims)
helper = nat.AlgorithmHelper(ftest,  genePool, fitness, environment = env)


Ngen = 10000
Npop = 10
Ncouples = 3

Nsurvive = 1
mutateThresold = 0.0001

algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive,  mutateThresold)
recorder = nat.basicRecorder(25, 1)
analysis = nat.Analysis(algorithm, recorder)

best1 = analysis.runAnalysis(Ngen)
nat.pickleAnalysis(analysis.currentGen, outputGen)





img = renderImg(*best1, dx,dy)

data = analysis.getRecorderData()
plt.plot(data.genNumber, data.bestScores)



# gen = nat.readPickle(inputGen)
# best1 = analysis.runAnalysis(Ngen, gen)


# =============================================================================
# 
# =============================================================================


# nat.plotAvgScore(data)
# nat.plotGeneValue(data, 2, 1)

imgPixel = np.array(img, float)
targetPixel = np.array(env.target)
diff = np.sum((imgPixel - targetPixel)**2)

test = imgPixel - targetPixel

# output = data.bestGenotypes
gifName = 'Naturalize.gif'

images = []
for genotype in data.bestGenotypes:
    img = renderImg(*genotype, dx,dy)
    images.append(img)
    
images[0].save(gifName,
               save_all = True, append_images = images[1:], 
               optimize = False, duration = 2)





# data = analysis.getRecorderData()
# nat.recorder.pickleAnalysis(data, 'DataPickle.P')