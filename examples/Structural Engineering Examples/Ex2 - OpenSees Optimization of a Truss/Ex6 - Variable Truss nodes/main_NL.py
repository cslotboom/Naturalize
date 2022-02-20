# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt
from functions import ftest, fitness, fitnessLength, fitnessComplex, environment, genePool, plotIndividual

np.random.seed(23)

# Define the environment, this range of possible locations for nodes
Ngrid = 201
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 11       # can be 10 or 11
forces = np.array([1000., 1000., 0.])
env = environment(Ngrid, xlims, ylims, trussMat, forces)


# Define the gene pool, this defines the range of genotypes an individual can have.
Nmax = Ngrid**2 - 1
llims = [np.array([0,0,0,0])]
ulims = [np.array([Nmax, Nmax, Nmax, Nmax])]
pool = genePool(llims, ulims)

# Define set the algorithm helper
helper = nat.AlgorithmHelper(ftest, pool, fitness, environment = env)

Ngen = 400
Npop = 100
Ncouples = 35
Nsurvive = 10
mutateThresold = 0.1

# define and run the analysis object
algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold, False)
recorder = nat.basicRecorder(1,5)
analysis = nat.Analysis(algorithm, recorder)
best = analysis.runAnalysis(Ngen)   


# nat.pickleAnalysis(Analysis, 'Truss.obj')
data = analysis.getRecorderData()

# =============================================================================
# 
# =============================================================================


# for gen in Analysis.gens:
#     plotIndividual(gen.best, env)
#     print(gen.best.genotype[0])
    
# Analysis = nat.readPickle('Truss3.obj')

for genotype in data.cumBestIndivduals[-5:]:
    plotIndividual(genotype, env)
    print(genotype)
# =============================================================================
# 
# =============================================================================

out = nat.readPickle('Truss.obj')
fig, ax = plt.subplots()
# nat.plotAvgFitness(fig, ax, out)
nat.plotMinFitness(fig, ax, out)
nat.plotTotalFitness(fig, ax, out)
# ax.set_ylim(0,3000)

Ngen = data.Ngen
# scoreBest = np.zeros(Analysis.Ngen)