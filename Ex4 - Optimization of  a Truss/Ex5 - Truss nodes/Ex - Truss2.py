# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as nat
import numpy as np
import os
import hysteresis as hys

import matplotlib.pyplot as plt
import openseespy.opensees as op

from functions import ftest, fitness

# np.random.seed(40)

xlims = np.array([0,5])
ylims = np.array([0,10])

Nnode = 4


genePool = nat.DefaultGenePool(llims, ulims)

helper = nat.AlgorithmHelper(ftest, fitness, genePool)

Ngen = 10
Npop = 100
Ncouples = 40
Nsurvive = 10
mutateThresold = 0.1

Analysis = nat.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
Analysis.optimize()
nat.pickleAnalysis(Analysis, 'Truss2.obj')

# =============================================================================
# 
# =============================================================================

out = nat.readPickle('Truss2.obj')
fig, ax = plt.subplots()
# test.plotAvgFitness(fig, ax, out)
nat.plotMinFitness(fig, ax, out)
nat.plotTotalFitness(fig, ax, out)
# ax.set_ylim(0,3000)