# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import numpy as np

import naturalize as nat
from functions import Environment, GenePool,ftest, fitness, crossover, mutate

start = 60
end = 520
np.random.seed(40)

# parameters
sparseness_of_map = 0.5
size_of_map = 1000
number_of_iterations = 1000
mutation_probability = 0.01
# number_of_groups = 1
env = Environment(sparseness_of_map, size_of_map)
genePool = GenePool(start, end, env.mapping)


helper = nat.AlgorithmHelper(ftest, fitness, genePool, mutate, crossover, environment=env)

Ngen = 40
Npop = 40
Ncouples = 8
Nsurvive = 2
mutateThresold = 0.1

Analysis = nat.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
Analysis.optimize()




