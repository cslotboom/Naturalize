# -*- coding: utf-8 -*-
"""
@author: Christian


"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt

from functions import ftest, fitness, fitnessLength,fitnessLength2, fitnessComplex, environment, genePool, plotIndividual, testIndividual

Ngrid = 201

Nmax = Ngrid**2 - 1

Nnodes = 8
Nconnect = int(Nnodes*(Nnodes - 1) / 2)
staticx = np.array([0,1, 1])
staticy = np.array([0,0, 3])

# Define the gene pool, this defines the range of genotypes an individual can have.
lx     = np.zeros(Nnodes)
ux     = np.ones(Nnodes)*1
ly     = np.zeros(Nnodes)
uy     = np.ones(Nnodes)*3.5

# Why multiplied by 2?
lconnectMask    = np.zeros(Nconnect)
uconnectMask    = np.ones(Nconnect)*2
lnodeMask       = np.zeros(Nnodes)
uNodeMask       = np.ones(Nnodes)*2

llims = [lx, ly, lconnectMask, lnodeMask]
ulims = [ux, uy, uconnectMask, uNodeMask]
# pool = nat.DefaultGenePool(llims, ulims)

pool = genePool(llims, ulims)
pool.setStaticNodes(staticx, staticy)


# Define the environment, this range of possible locations for nodes
# Ngrid = 201
trussMat = 10       # can be 10 or 11
forces = np.array([1000., 1000., 0.])
fmut = nat.getMutate(1)
env = environment(Ngrid, trussMat, forces, Nnodes, len(staticx))
helper = nat.AlgorithmHelper(ftest, pool, fitnessLength, fmut, environment = env)

Ngen = 1000
Npop = 30
Ncouples = 8
Nsurvive = 1
mutateThresold = 0.025

# define and run the analysis object
algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive,  mutateThresold)
recorder = nat.basicRecorder(10,1)
analysis = nat.Analysis(algorithm, recorder)
best = analysis.runAnalysis(Ngen)

# =============================================================================
# 
# =============================================================================
data = analysis.getRecorderData()
plt.plot(data.genNumber, data.bestScores)

plotIndividual(data.bestIndividuals[-1], env)

for indv in data.bestIndividuals:
    plotIndividual(indv, env)
    # plt.annotate(round(score,4), [0.,3])
    
# for indv,score in zip(data.populations[-1],data.populationBestScores[-1]):
#     fig, ax = plotIndividual(indv, env)
#     plt.annotate(round(score,4), [0.,3])
#     plt.annotate(round(score,4), [0.,3])
#     plt.show()


# testIndividual(data.populations[-1][-5], env)
# fig, ax = plotIndividual(data.populations[-1][-5], env)
# plt.annotate(round(score,4), [0.,3])
# testIndividual(data.populations[-1][-5], env)




# for gen in Analysis.gens:
#     plotIndividual(gen.best, env)
#     print(gen.best.genotype[0])
    
# Analysis = nat.readPickle('Truss.obj')

# for genotype in Analysis.cumBestIndivduals[-5:]:
#     plotIndividual(genotype, env)
    # print(genotype)
# =============================================================================
# 
# =============================================================================

# out = nat.readPickle('Truss.obj')
# fig, ax = plt.subplots()
# nat.plotAvgFitness(fig, ax, out)
# nat.plotMinFitness(fig, ax, Analysis)
# nat.plotTotalFitness(fig, ax, Analysis)
# ax.set_ylim(0,3000)

# Ngen = Analysis.Ngen
# scoreBest = np.zeros(Analysis.Ngen)

# for ii in range(Ngen):              
#     scoreBest[ii] = np.min(Analysis.gens[ii].scores)