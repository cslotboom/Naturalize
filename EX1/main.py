# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import baseFunctions as bf
import numpy as np


start = 60
end = 520
np.random.seed(40)

# parameters
sparseness_of_map = 0.5
size_of_map = 1000
population_size = 40
number_of_iterations = 1000
NReproducingCouples = 8
Nsurvive = 2
mutation_probability = 0.01
# number_of_groups = 1
    
# initialize the map and save it
mapping = bf.init_map(sparseness_of_map, size_of_map)


# create the starting population
population = bf.generate_Starting_Population(population_size, start, end, mapping)

last_distance = 1000000000
# for a large number of iterations do:

mutateThresold = 0.01


# import numpy as np
# from itertools import combinations
# def TSP(G):
#    n = len(G)
#    C = [[np.inf for _ in range(n)] for __ in range(1 << n)]
#    C[1][0] = 0 # {0} <-> 1
#    for size in range(1, n):
#       for S in combinations(range(1, n), size):
#           S = (0,) + S
#           k = sum([1 << i for i in S])
#           for i in S:
#     	      if i == 0: continue
#     	      for j in S:
#                   if j == i: continue
#                   cur_index = k ^ (1 << i)
#                   C[k][i] = min(C[k][i], C[cur_index][j]+ G[j][i])     
# 		                                       #C[S−{i}][j]
#    all_index = (1 << n) - 1
#    return min([(C[all_index][i] + G[0][i], i) \
#                             for i in range(n)])


# TSP(mapping)


for ii in range(150):
    new_population = []
    
    # evaluate the fitness of the current population
    scores = bf.score_population(population, mapping)
    fitnessProbs = bf.get_fitness_probailities(scores)

    best = population[np.argmin(scores)]
    number_of_moves = len(best)
    distance = bf.fitness(best, mapping)
    
    if distance != last_distance:
        print('Iteration %i: Best so far is %i steps for a distance of %f' % (ii, number_of_moves, distance))
        bf.plot_best(mapping, best, ii, start, end)

    
    # Here we curate the population with some rules.
    # We first pick surviving genes by allowing the existing population to reproduce.
    # allow members of the population to reporuduce based on their relative score; 
    # i.e., if their score is higher they're more likely to reproduce
    for jj in range(NReproducingCouples):  
        mate1 = population[bf.pick_mate(scores, fitnessProbs)]
        mate2 = population[bf.pick_mate(scores, fitnessProbs)]
        
        new_1, new_2 = bf.crossover(mate1, mate2, start, end)
        new_1 = bf.mutate(new_1, mutateThresold, mapping, end)
        new_2 = bf.mutate(new_1, mutateThresold, mapping, end)
        
        new_population = new_population + [new_1, new_2]

    # keep the best members of previous generation
    new_population += [population[np.argmin(scores)]]
    for jj in range(Nsurvive):
        keeper = bf.pick_mate(scores, fitnessProbs)            
        new_population += [population[keeper]]
        
    # add new random members
    while len(new_population) < population_size:
        new_population += [bf.genereateValidRoute(start, end, mapping)]
        
    #replace the old population with a real copy
    # population = copy.deepcopy(new_population)
    population = new_population
            
    last_distance = distance
        
    # plot the results