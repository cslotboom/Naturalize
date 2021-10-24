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
    
    The environment stores conditions universal to all individuals. 
    
    For example, some problems may require comparing to data found in a file.
    The environment could be used to read that file data, allowing each 
    solution to have access to that data.   
    
    """
    
    def __init__(self):
        """
        The generic problem doesn't need an environment
        """

        pass

def defaultFitness(individual, env):
    """ In this case getting fitness from our result is trivial
    """       
    
    return individual.result

def namePopulation(population, gen):
    """
    For each individual in the population, assign a name.
    """
    
    for ii, individual in enumerate(population):
        individual.name = int(ii)
        individual.gen = int(gen)

# =============================================================================
# Default evaluation functions
# =============================================================================
"""
Thes functions are used to work with individual containers
"""

def _rankFitness(scores, Npop):
    
    """
    Assign a rank to each item in the population, with low scors being assigned
    the first rank.
    
      [0, 1, 100, 20, 0.1, 5]   - >    [0, 2, 5, 4, 1, 3]
    
    """
    
    # find wich scores should be combined
    # Scores with a low fitness should be combined at higher probability
      
    populationRanks = np.zeros(Npop)
    # print(scores)
    # sort the array, then create an array of ranks
    sortedIndexes = scores.argsort()    
    populationRanks[sortedIndexes] = np.arange(Npop)
    return populationRanks

def _rankFitnessInversed(scores, Npop):
    """
    Assign a rank to each item in the population, with high scores being assigned
    the highest rank.
    
      [0, 1, 100, 20, 0.1, 5]   - >    [5, 3, 0, 1, 4, 2]
      
    Parameters
    ----------
    scores : list
        A list of input scores input scores.
    Npop : TYPE
        THe number of individuals in the population.

    Returns
    -------
    float
        The ranks in order of highest output to lowest output.

    """
          
    ranks = _rankFitness(scores, Npop)
    return Npop - ranks


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

            