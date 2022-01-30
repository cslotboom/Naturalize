# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""


import os
import numpy as np
from .solutionClass import Individual, Generation, BasicGenePool

# from .defaultFuncs import (initPopulation, defaultEnvironment, 
#                            defaultCrossover, defaultMutate, 
#                            defaultFitnessProbs, pick_Individual, 
#                            namePopulation)
import pickle 

import matplotlib.pyplot as plt



class dataReader():
    
    def __init__(self, data, function):
        """
        A generic way of getting the output from our datastructure.
        
        Assume that the population is always the same.
        """        
        
        self.data = data
        self.f = function
        
        self.Ngen = len(data.populations)
        self.Npop = len(data.populations[0])
        

    def get(self, *args):
        output = [None]*self.Ngen
        for ii, indv in enumerate(self.data.populations):
            output[ii] = self.f(indv, self.Npop, *args)
            
        return np.array(output)




def getPopAvg(population, Npop):
    
    score = np.zeros(Npop)
    for ii in range(Npop):
        score[ii] = population[ii].result
        
    return np.average(score)

def getGeneValue(population, Npop, indGeontype, indGene):
    """
    Reads from our generic gene structure
    """
    
    genes = np.zeros(Npop)
    for ii in range(Npop):
        genes[ii] = population[ii].genotype[indGeontype][indGene]
        
    return genes

def getGeneAvg(population, Npop, indGeontype, indGene):
    """
    Reads from our generic gene structure
    """
    
    genes = np.zeros(Npop)
    for ii in range(Npop):
        genes[ii] = population[ii].genotype[indGeontype][indGene]
        
    return np.average(genes)


# def getScoreAvg(data):

#     Ngen = len(data.populations)
#     Npop = len(data.populations[0])
    
#     avg = np.zeros(Ngen)
#     for ii, pop in enumerate(data.populations):
#         avg[ii] = getPopAvg(pop,Npop)
        
#     return avg        





# def getGeneAvg(data, Npop):

#     score = np.zeros(Npop)
#     for ii, pop in enumerate(data.populations):
#         avg[ii] = getPopAvg(pop,Npop)
        
#     return avg
        




# =============================================================================
# 
# =============================================================================


def plotAvgScore(data):
    
    #Check data??
    
    # reader = dataReader(data, getPopAvg)
    # avg = reader.get()
    avg = np.average(data.populationBestScores, 1)
    x = data.genNumber
   
    line = plt.plot(x, avg)
    return line


def plotGeneValue(data, indGenotype:int, indGene:int):
    
    reader = dataReader(data, getGeneValue)
    genes = reader.get(indGenotype, indGene)
    
    x = data.genNumber
    fig, ax = plt.subplots()
    plt.plot(x,genes, '.', linewidth = 0)
    
    return fig, ax
    
    # return gener
    
def plotAvgGeneValue(data, indGenotype:int, indGene:int):
    
    reader = dataReader(data, getGeneAvg)
    avg = reader.get(indGenotype, indGene)
    
    x = data.genNumber
    line = plt.plot(x,avg)
    
    return line

    
def plotGeneValues(data):
    pass


def plotGeneAvg(data):
    pass    
    
