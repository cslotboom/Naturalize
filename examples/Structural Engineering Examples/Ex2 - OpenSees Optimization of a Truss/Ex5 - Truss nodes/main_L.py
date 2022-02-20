# -*- coding: utf-8 -*-
R"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian

In this example, the node positions are optimized by . 
Three nodes are fixed in the example, the top most node, and the two bottom
nodes.
The connectivity between nodes is also fixed.


"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt

from functions import ftest, fitness, fitnessLength, fitnessComplex, environment, genePool, plotIndividual

Ngrid = 201
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([1000., 1000., 0.])
env = environment(Ngrid, xlims, ylims, trussMat, forces)

# Define the gene pool, this defines the range of genotypes an individual can have.
llims = [np.array([0,0,0,0]), np.array([0,0,0,0])]
ulims = [np.array([1, 1, 1, 1]),np.array([2, 2, 2, 2])]
pool = nat.BasicGenePool(llims, ulims)

# Define set the algorithm helper
helper = nat.AlgorithmHelper(ftest, pool, fitness, environment = env)

Ngen = 100
Npop = 50
Ncouples = 20
Nsurvive = 1
mutateThresold = 0.2

# define and run the analysis object
algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold)
recorder = nat.basicRecorder(1,5)
analysis = nat.Analysis(algorithm, recorder)
best = analysis.runAnalysis(Ngen)   
# nat.pickleAnalysis(analysis, 'Truss.obj')


data = analysis.getRecorderData()
plt.plot(data.genNumber, data.bestScores)

# data.bestIndivduals[-1]
plotIndividual(data.bestIndividuals[-1], env)

for indv in data.bestIndividuals:
    plotIndividual(indv, env)
    # print(gen.best.genotype[0])

