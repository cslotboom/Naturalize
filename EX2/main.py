# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import env as env
import numpy as np
import os

import hysteresis.hys as hys
import matplotlib.pyplot as plt


# np.random.seed(40)

inches = 0.0254
kip = 4.45*1000

# parameters
Npopulation = 30
Ngen = 50
NReproducingCouples = 8
Nsurvive = 2
mutateThresold = 0.1
# number_of_groups = 1

llims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 0.
ulims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 1.5

    
# initialize the map and save it
environment = env.Environment(llims, ulims)
genePool = env.GenePool(llims, ulims)


# create the starting population
population = env.initPopulation(genePool, Npopulation)

# Import Experimental Data here
EDataName = "BackboneData.csv"
ExperimentData = np.loadtxt(EDataName,delimiter=',')

Backbonex = ExperimentData[:,0]*inches
Backboney = ExperimentData[:,1]*kip


xyExp = np.column_stack([Backbonex, Backboney])
hys2 = hys.Hysteresis(xyExp)

last_distance = 1000000000
# for a large number of iterations do:


for ii in range(Ngen):
    
    env.reNamePopulation(population, int(ii))
   
    # make directory
    gen = 'gen' + str(int(ii))
    
    if not os.path.isdir(gen):
        os.mkdir(gen)
        
    new_population = []
    for jj in range(Npopulation):
        # print(population[jj].genome)
        environment.testIndividual(population[jj])
    
    
    # evaluate the fitness of the current population
    scores = env.score_population(population, environment, hys2)
    fitnessProbs = env.get_fitness_probailities(scores)

    best = population[np.argmin(scores)]
    # number_of_moves = len(best)
    distance = scores[np.argmin(scores)]
    
    if best != last_distance:
        print('Iteration %i: Best so far is a distance of %f' % (ii, distance))
        print(best.genome)
        xy = population[np.argmin(scores)].getxy()
        fig, ax = plt.subplots()
        plt.plot(xy[:,0], xy[:,1])
        # plot_best(mapping, best, gen, start, end)

    
    # Here we curate the population with some rules.
    # We first pick surviving genes by allowing the existing population to reproduce.
    # allow members of the population to reporuduce based on their relative score; 
    # i.e., if their score is higher they're more likely to reproduce
    for jj in range(NReproducingCouples):  
        mate1 = env.pick_mate(population, scores, fitnessProbs)
        mate2 = env.pick_mate(population, scores, fitnessProbs)
    
        # mate2 = population[env.pick_mate(scores, fitnessProbs)]
        
        new_1, new_2 = env.crossover(mate1, mate2)
        new_1 = env.mutate(new_1, mutateThresold, genePool)
        new_2 = env.mutate(new_2, mutateThresold, genePool)
        
        new_population = new_population + [new_1, new_2]

    # keep the best members of previous generation
    new_population += [population[np.argmin(scores)]]
    for jj in range(Nsurvive):
        keeper = env.pick_mate(population, scores, fitnessProbs)            
        new_population += [keeper]
        
    # add new random members
    while len(new_population) < Npopulation:
        newGenome = genePool.getGenome()
        new_population += [env.Individual(newGenome)]
        
    # #replace the old population with a real copy
    # # population = copy.deepcopy(new_population)
    population = new_population
            
    # last_distance = distance
    
    # return population
