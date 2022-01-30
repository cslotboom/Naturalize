# -*- coding: utf-8 -*-
"""
This basic example shows how naturalize can be used to optimize a basic 
functions. We will optimzie the following equation, where each variable ranges
from -10 to 10:
    f(x,y,z) = x*y + z

"""

"""
First we import the libraries we will use and set the random 
seed for reproducibility.
"""
import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(60)

"""
Next we will define a function for the problem we wish to optimize. In this 
case it is a simple straightforward multivariable equation.

The environment class should contain all information we want to have access to
when evaulating each individual genome. In this case we only need our objective
function.
"""

def objectiveFunction(x, y, z):
    return x*y + (z)

class Environment:
    test = objectiveFunction

"""
Next we will define the gene pool that all solutions can be drawn from. This 
involves selecting the "shape" of the problem genotype, as well as it's bounds.

Geonotypes are made up of a number of gene units, and each unit is made up of 
numbers or numpy arrays. In this simple example, we represent the problem with
a single gene, that has three units. In this unit, the gene values are bounded
between -10 and 10 according to our problem definition.
"""

genomeLB = [np.array([-10, -10, -10]) ]
genomeUB = [np.array([10, 10, 10]) ]
genePool = nat.BasicGenePool(genomeLB, genomeUB)

"""
We can make a sample genotype and individual.
"""
sampleGenotype = genePool.getNewGenotype()
sampleIndividual = nat.Individual(sampleGenotype)

"""
The next step is to define a test function for the problem. This function
'tests' each indivdual by taking their genotype, applying it to the problem, 
and recording the raw result.

The test fuction always takes in two variables, the individual and the 
environment. 

In this problem we could hav skipped using the environment, but it's generally
easier to have a in one place.

"""

def ftest(individual, env):
    x,y,z = individual.genotype[0]
    return env.test(x, y, z)


"""
Next we define the analysis parameters. This includes the number of generations
to use in the analysis, population size, survivors, and couples.
Survivers don't get modified between generations, while couples are the number
of paired individuals that will reproduce.

The mutation threshold determines how likely each gene unit is to mutate.

"""

Ngen = 1000
Npop = 30
Ncouples = 13
Nsurvive = 1
mutThresold = 0.3

helper    = nat.AlgorithmHelper(ftest, genePool, environment = Environment)
algorithm = nat.GeneticAlgorithm(Npop, Ncouples, Nsurvive, helper, mutThresold)

"""
We define a recorder for the analysis, this determines how often data is saved, 
and what data is saved. We'll save the 15 best indivduals every 5 generations.
"""
recorder = nat.basicRecorder(5, 15)

"""
Next we will create and run the analysis.
"""
analysis = nat.Analysis(algorithm, recorder)
bestGenotype = analysis.runAnalysis(Ngen)

print(bestGenotype)


"""
We can also save the analysis. It can be loaded and run from this point later.
"""

data = analysis.getRecorderData()
nat.pickleAnalysis(data, 'DataPickle.P')

# =============================================================================
# Plotting
# =============================================================================


plt.plot(data.genNumber, data.bestScores)
line = nat.plotAvgScore(data)

fig, ax = plt.subplots()
lines = nat.plotGeneValue(data, 0, 2)

fig, ax = plt.subplots()
lines = nat.plotAvgGeneValue(data, 0, 1)
