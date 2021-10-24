# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""

import numpy as np
from .solutionClass import Individual



def initPopulation(size, genePool):
    """ Creates the first generation of the population"""
    gen = 0
    population = []
    for ii in range(size):
        genotype = genePool.getNewGenotype()
        population.append(Individual(genotype))
        
    namePopulation(population, gen)
        
    return population


class defaultEnvironment:
    """
    Stores conditions universal to all individuals.
    """
    
    def __init__(self):

        pass



def defaultFitness(individual, env):
    """ In this case getting fitness from our result is trivial
    """       
    
    return individual.result




def mutateGene(individual, oldGene, tempGene, threshold):
            # for each value we randomly mutate depeding on the threshold.
        N = len(oldGene)
        Pvector = np.random.random_sample(N)
        
        # Get the genotype and a new genotype

        newGene = np.zeros(N)
        # Find the first value less than the threshold
        
        # Find the values that were mutated, assign them values form the new gene.
        mutateIndexes = np.where(Pvector < threshold)
        newGene[mutateIndexes] = tempGene[mutateIndexes]
        
        
        mask = np.ones(N, np.bool)
        mask[mutateIndexes] = 0
        newGene[mask] = oldGene[mask]
        
        return newGene
        


def defaultMutate(individual, threshold, GenePool):
    
    """
    Mutate will randomly generate a new solution based on the old solution.
    
    The default mutate function generates valid solutions where the solution
    is an array of inputs:
        X = [x1, x2, x3, ..., xN]
    
    And, that array for two valid solutions X and Y, the solution Z is also a 
    solution
        Z = [y1, x2, x3, y4, ..., yN]
 
    """   
    
    # Given an individual, randomly create a new solution
    Ngenes = len(individual.genotype)
    newGenotype = [None]*Ngenes
    tempGenotype = GenePool.getNewGenotype()
    
    for ii in range(Ngenes):
        oldGene = individual.genotype[ii]
        tempGene    = tempGenotype[ii]
        newGenotype[ii] = mutateGene(individual, oldGene, tempGene, threshold)

    
    return Individual(newGenotype)


# =============================================================================
# Default evaluation functions
# =============================================================================
"""
Thes functions are used to work with individual containers
"""

def _rankFitness(scores, Npop):
    # find wich scores should be combined
    # Scores with a low fitness should be combined at higher probability
      
    populationRanks = np.zeros(Npop)
    # print(scores)
    # sort the array, then create an array of ranks
    sortedIndexes = scores.argsort()    
    populationRanks[sortedIndexes] = np.arange(Npop)

    # the inverse of the fitness rank
    # return Npop - populationRanks
    return populationRanks

# def _getRouleteArea

def defaultFitnessProbs(scores):
    
    """
    This works for any possible value of scores.
    
    The probability of each selection is assigned, assuming we wish to minimize scores.
    
    This takes the score and assignes a rank 1-N based on the score.
    A cumulative distribution is then created by summing the inverse of each rank
    and dividing by the total sum of ranks.
    
    Each point in the output array has width equal to the liklihood of it being
    chosen.
    
    
    """
    Npop = len(scores) 
    populationRanks = _rankFitness(scores, Npop)
    
    
    wheelAreas = Npop - populationRanks
    cumulativeFitness = np.cumsum(wheelAreas)
    probs = cumulativeFitness / cumulativeFitness[-1]
    
    return probs

def pick_Individual(population, probs):
    
    """
    Randomly selects individuals using rullette wheel apprach and a set of 
    probabilities
    """
    
    # Select a mamber of the pupulation at random depending on the ranked probability
    rand = np.random.random()
    selection = population[np.argmax(rand < probs)]
    return selection

def namePopulation(population, gen):
    
    for ii, individual in enumerate(population):
        individual.name = int(ii)
        individual.gen = int(gen)
            