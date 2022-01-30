# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 23:21:46 2022

@author: Christian
"""

import naturalize as nat

def objectiveFunction(x, y, z):
    """ The function we wish to minimize """
    return x*y + (z)

def ftest(individual, env):
    """ The function that will get applied to each individual. """
    return objectiveFunction(*individual.genotype[0])
    
lowerBounds = [-10, -10, -10]    # minimum values on each gene
upperBounds = [10, 10, 10]       # the maximum value on each gene

Ngen = 100              # Number of generations for the analysis
Npop = 30               # The population of each generaton
Ncouples = 10           # The number of couples - each makes two offspring
Nsurvive = 1            # The number of unmodified survivors

# Define the analysis objects.
genePool  = nat.BasicGenePool(lowerBounds, upperBounds)
helper    = nat.AlgorithmHelper(ftest, genePool)
algorithm = nat.GeneticAlgorithm(helper, Npop, Ncouples, Nsurvive)
analysis  = nat.Analysis(algorithm)
solution  = analysis.runAnalysis(Ngen)
print(solution)

File = 'Test.json'
myDict = nat.algorithm.generationToDict(analysis.currentGen)
nat.algorithm.generationToJson(analysis.currentGen, File)
test = nat.algorithm._loadJson(File)

