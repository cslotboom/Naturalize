# -*- coding: utf-8 -*-
R"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian

In this example, the node positions are optimized by . 
Three nodes are fixed in the example, the top most node, and the two bottom
nodes.
The connectivity between nodes is also fixed.


"""

"""
Import functions and set the random seed for reproducability.
"""
import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt
from functions import ftest, fitness_basic, fitness_Complex, environment, plotIndividual

dataName = 'Analysis data.P'

xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([10000., 1000., 0.])
env = environment(xlims, ylims, trussMat, forces)

"""
Set up the gene pool. Two genes will be used, one for the x position of each
node, and one for the y position of each node.
"""

llims = [np.array([0,0,0,0]), np.array([0,0,0,0])]
ulims = [np.array([1, 1, 1, 1]),np.array([2, 2, 2, 2])]
pool = nat.BasicGenePool(llims, ulims)


"""
Define population size. A fairly large sample size is used. We use a mutation
rate of about 1/N_gene.
"""
helper = nat.AlgorithmHelper(ftest, pool, fitness_Complex, environment = env)

Ngen = 1000
Npop = 25
Ncouples = 12
Nsurvive = 0
mutateThresold = 0.065

"""
Define the algorithm, analysis, and a recoder.
"""
algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive, mutateThresold)
recorder = nat.basicRecorder(5, 5)
analysis = nat.Analysis(algorithm, recorder)
best = analysis.runAnalysis(Ngen)   

"""
Save the analyisis to a pickle and plot the output data. It's often useful to 
see how the results of the analysis are changing over time.'
"""
data = analysis.getRecorderData()
nat.pickleData(data, dataName)
plt.plot(data.genNumber, data.bestScores)
plotIndividual(data.bestIndividuals[-1], env)

