# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as test
import numpy as np
import os

import matplotlib.pyplot as plt

from functions import ftest, fitness


np.random.seed(40)
llims = [np.array([-10, -10, -10])]
ulims = [np.array([10, 10, 10])]
genePool = test.DefaultGenePool(llims, ulims)


helper = test.AlgorithmHelper(ftest, fitness, genePool)

Ngen = 100
Npop = 30
Ncouples = 10
Nsurvive = 2
mutateThresold = 0.1

Analysis = test.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
Analysis.optimize()

test.pickleAnalysis(Analysis, 'TestFile.obj')
Analysis = test.readPickle('TestFile.obj')

fig, ax = plt.subplots()
test.plotAvgFitness(fig, ax, Analysis)
test.plotMinFitness(fig, ax, Analysis)
test.plotTotalFitness(fig, ax, Analysis)





# yAvg = np.zeros(Ngen)
# ybest = np.zeros(Ngen)
# scoreAvg = np.zeros(Ngen)
# scoreBest = np.zeros(Ngen)

# BestOverTime = np.zeros(Ngen)

# for ii in range(Ngen):
#     # Get the genome
#     out = np.array(algorithm.gens[ii].getCurrentGenome())
#     yAvg[ii] = -np.average(out[:,1])
#     ybest[ii] = -np.min(out[:,1])
    
#     scoreAvg[ii] = -np.average(algorithm.gens[ii].scores)
    
#     scoreBest[ii] = -np.min(algorithm.gens[ii].scores)
#     scoreBest[ii] = -np.min(algorithm.gens[ii].scores)
    
# BestOverTime = algorithm.BestValues
# print(algorithm.gens[5].getCurrentGenome())

# fig, ax = plt.subplots()
# plt.plot(yAvg)
# plt.plot(ybest)

# fig, ax = plt.subplots()
# plt.plot(scoreAvg)
# plt.plot(scoreBest)
# plt.plot(-BestOverTime)
