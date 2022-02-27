# -*- coding: utf-8 -*-
R"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian

This script keeps crashing at random times!
After much debugging, I suspect it is a memory issue


"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt

from functions import ftest, fitness, fitnessLength, fitnessComplex, environment, genePool, plotIndividual
import openseespyvis.Get_Rendering

import openseespyvis.styles as s


ele_style = {'color':'black', 'linewidth':2, 'linestyle':'-'} # elements
myStyle = s.customStyle(ele_style = ele_style)
openseespyvis.Get_Rendering.style = myStyle
# style
# np.random.seed(300)

# Define the environment, this range of possible locations for nodes
Ngrid = 201
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([1000., 1000., 0.])
env = environment(Ngrid, xlims, ylims, trussMat, forces)


# Define the gene pool, this defines the range of genotypes an individual can have.
llims = [np.array([0,0,0,0]), np.array([0,0,0,0])]
ulims = [np.array([1, 1, 1, 1]),np.array([2, 2, 2, 2])]
# pool = genePool(llims, ulims)
pool = nat.DefaultGenePool(llims, ulims)

# Define set the algorithm helper
# helper = nat.AlgorithmHelper(ftest, fitnessComplex, pool, environment = env)
helper = nat.AlgorithmHelper(ftest, fitnessLength, pool, environment = env)
# helper = nat.AlgorithmHelper(ftest, fitnessComplex, pool, environment = env)
# Define the anaysis parameters


Ngen = 30
Npop = 50
Ncouples = 15
Nsurvive = 2
mutateThresold = 0.125

# define and run the analysis object
algorithm = nat.GeneticAlgorithm(Npop, Ncouples, Nsurvive, helper, mutateThresold)
# recorder = nat.liteRecorder(2)
recorder = nat.basicRecorder(1,5)

analysis = nat.Analysis(algorithm, recorder)

best = analysis.runAnalysis(Ngen)   
nat.pickleAnalysis(analysis, 'Truss.obj')


data = analysis.getRecorderData()
plt.plot(data.genNumber, data.bestScores)

# data.bestIndivduals[-1]
plotIndividual(data.bestIndivduals[-1], env)

for indv in data.bestIndivduals:
    plotIndividual(indv, env)
    # print(gen.best.genotype[0])

# =============================================================================
# 
# =============================================================================

# for gen in Analysis.gens:
#     plotIndividual(gen.best, env)
#     print(gen.best.genotype[0])
    
# Analysis = nat.readPickle('Truss3.obj')

# for genotype in Analysis.cumBestIndivduals[-5:]:
#     plotIndividual(genotype, env)
#     print(genotype)
# # =============================================================================
# # 
# # =============================================================================

# # out = nat.readPickle('Truss.obj')
# fig, ax = plt.subplots()
# # nat.plotAvgFitness(fig, ax, out)
# nat.plotMinFitness(fig, ax, Analysis)
# nat.plotTotalFitness(fig, ax, Analysis)
# # ax.set_ylim(0,3000)

# Ngen = Analysis.Ngen
# scoreBest = np.zeros(Analysis.Ngen)

# for ii in range(Ngen):              
#     scoreBest[ii] = np.min(Analysis.gens[ii].scores)