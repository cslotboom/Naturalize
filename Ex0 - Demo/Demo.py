# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

An example showing how naturalize can be used to solve basic functions.

@author: Christian
"""


"""
Here we import our functions and set the random seed for reproducibility 
"""

import naturalize as nat
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(40)



"""
Our test functions is defined. The test fuction takes in two variables, the
individual and the environment.

Note that the objective function has been seperated out for convenience. It's
often useful to seperate the - we may wish to further process our result.

Can we simplify this with a 

"""

def objectiveFunction(x, y, z):
    """ The function we wish to minimize """
    return x*y + (z)

def ftest(individual, env):
    """
    The function that will get applied to each individual.
    """
    individual.result = objectiveFunction(*individual.genotype[0])
    return individual.result


lowerBounds = np.array([-10, -10, -10])     # minimum values on each gene
upperBounds = np.array([10, 10, 10])        # the maximum value on each gene
Ngen = 100              # Number of generations for the analysis
Npop = 30               # The population of each generaton
Ncouples = 10           # The number of couples - each makes two offspring
Nsurvive = 1            # The number of unmodified survivors
recordGen = 5           # The time between a generation being recorded 
Nrecord   = 15          # The number of individuals to record in the generation.

# Define the analysis objects. We
genePool  = nat.BasicGenePool(lowerBounds, upperBounds)
helper    = nat.AlgorithmHelper(ftest, genePool = genePool)
algorithm = nat.GeneticAlgorithm(Npop, Ncouples, Nsurvive, helper)
recorder  = nat.basicRecorder(5, 15)

analysis = nat.Analysis(algorithm, recorder)
solution = analysis.runAnalysis(Ngen)
print(solution)

data = analysis.getRecorderData()


# =============================================================================
# Plotting
# =============================================================================


plt.plot(data.genNumber, data.bestScores)
# line = nat.plotAvgScore(data)

