# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as test
import numpy as np
import os
import hysteresis as hys

import matplotlib.pyplot as plt

from functions import ftest, fitness

# np.random.seed(40)
llims =  np.ones(11)*0.
ulims =  np.ones(11) * 1.

genePool = test.DefaultGenePool(llims, ulims)

helper = test.AlgorithmHelper(ftest, fitness, genePool)

Ngen = 10
Npop = 100
Ncouples = 40
Nsurvive = 10
mutateThresold = 0.1

Analysis = test.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
Analysis.optimize()
test.pickleAnalysis(Analysis, 'Truss2.obj')

# =============================================================================
# 
# =============================================================================

out = test.readPickle('Truss2.obj')
fig, ax = plt.subplots()
# test.plotAvgFitness(fig, ax, out)
test.plotMinFitness(fig, ax, out)
test.plotTotalFitness(fig, ax, out)
# ax.set_ylim(0,3000)