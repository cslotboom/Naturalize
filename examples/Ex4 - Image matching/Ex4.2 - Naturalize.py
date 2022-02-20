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

inputGen  = 'Gen550000.P'
outputGen = 'Gen600000.P'
Ngen = 50000
outputData= 'Data_550-600-1-0.00025.P'
gifName = 'Naturalize_12.gif'


dx = 252
dy = 204
ImageName = 'Ex4.2-target.jpg'

env = Environment(dx,dy, ImageName)
Ncircle = 2500
rmin = 1
rmax = 10
lims = np.array([dx, dy, rmax, 255])

llims =  [np.zeros(Ncircle), np.zeros(Ncircle), np.ones(Ncircle)*rmin, np.zeros(Ncircle) * 0.]
ulims =  [np.ones(Ncircle)*dx, np.ones(Ncircle)*dy, np.ones(Ncircle)*rmax, np.ones(Ncircle)*255]
# fmut = nat.getMutate(1, p = 0.1)


genePool = nat.BasicGenePool(llims, ulims)
fmut = nat.getMutate(1)
helper = nat.AlgorithmHelper(ftest,  genePool, fitness, fmut, environment = env)

Npop = 10
Ncouples = 4
Nsurvive = 1
mutateThresold = 0.000025

algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive,  mutateThresold)
recorder = nat.basicRecorder(100, 1)
analysis = nat.Analysis(algorithm, recorder)

gen = nat.readPickle(inputGen)
best1 = analysis.runAnalysis(Ngen, gen)
data = analysis.getRecorderData()
nat.pickleData(data, outputData)
nat.pickleData(analysis.currentGen, outputGen)
# nat.saveCurrentGen(analysis, fileName)
plt.plot(data.genNumber, data.bestScores)
img = renderImg(*best1, dx,dy)
# =============================================================================
# 
# =============================================================================


nat.plotAvgScore(data)
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
    
images[0].save(gifName,
               save_all = True, append_images = images[1:], 
               optimize = False, duration = 2)





# data = analysis.getRecorderData()
# nat.recorder.pickleAnalysis(data, 'DataPickle.P')