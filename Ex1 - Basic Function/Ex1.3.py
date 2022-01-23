# -*- coding: utf-8 -*-
"""
This basic example shows some more advanced features of naturalize using
the basic function example. This includes
    - Continuing the analysis with different settings.
    - reloading a saved analysis

"""

"""
The initial portion of the problem is defined similarly to the last problem
"""
import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(40)

def objectiveFunction(x, y, z):
    return x*y + (z)

class userEnvironment:
    def __init__(self):
        self.test = objectiveFunction

genomeLB = [np.array([-10, -10, -10]) ]
genomeUB = [np.array([10, 10, 10]) ]
genePool = nat.BasicGenePool(genomeLB, genomeUB)

def ftest(individual, env):
    x,y,z = individual.genotype[0]
    return env.test(x, y, z)

helper = nat.AlgorithmHelper(ftest,  genePool, environment = userEnvironment())

"""
One useful feature of Natrualize is the ability to swap out algorithms in the 
analysis. We can re-write the algorithm of an an existing analysis using the 
set command.

Here we define two algorithms for the analysis, each using a different number
of couples.

"""


Ngen = 100
Npop = 30
Ncouples = [13, 5, 5]
Nsurvive = 1
mutThresold = [0.3, .3, .1]
mutThresold2 = 0.1

algorithm_1 = nat.GeneticAlgorithm(Npop, Ncouples[0], Nsurvive, helper, mutThresold[0])
algorithm_2 = nat.GeneticAlgorithm(Npop, Ncouples[1], Nsurvive, helper, mutThresold[1])
algorithm_3 = nat.GeneticAlgorithm(Npop, Ncouples[2], Nsurvive, helper, mutThresold[2])
recorder = nat.basicRecorder(5, 15)

analysis = nat.Analysis(algorithm_1, recorder)
best1 = analysis.runAnalysis(Ngen)


"""
We pickle the analysis data at the final generaton and restart the analysis
using a different algorithm
"""
dataName = 'DataPickle.P'
savedGen = analysis.getCurretGen()
nat.pickleAnalysis(savedGen, dataName)

analysis.setAlgorithm(algorithm_2)
gen   = nat.readPickle(dataName)
best2 = analysis.runAnalysis(Ngen, initialGen = gen)


"""
We can also swap out the algorithm in a active model. Plotting the data,
the differences between both can be observed.
"""

analysis.setAlgorithm(algorithm_1)
best2 = analysis.runAnalysis(Ngen)

data = analysis.getRecorderData()
fig, ax = plt.subplots()
lines = nat.plotGeneValue(data, 0, 2)

"""
We could also take a snapshot of the currentGeneration, and run several analyses
from that point.
"""

gen   = analysis.getCurretGen()

best1 = analysis.runAnalysis(Ngen, initialGen = gen)

analysis.setAlgorithm(algorithm_2)
best2 = analysis.runAnalysis(Ngen, initialGen = gen)

analysis.setAlgorithm(algorithm_3)
best3 = analysis.runAnalysis(Ngen, initialGen = gen)




