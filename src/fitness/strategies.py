# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""

import numpy as np
from .solutionClass import Individual



def defaultFitness(individual, env):
    """ In this case getting fitness from our result is trivial
    """       
    
    return individual.result


# =============================================================================
# Default evaluation functions
# =============================================================================
"""
Thes functions are used to work with individual containers
"""

def _rankFitness(scores, Npop):
    """
    Rank the population dependin on the scores.
    Scores with a high fitness will be combined with a higher probability
    """
    # find wich scores should be combined
    # Scores with a low fitness should be combined at higher probability
      
    populationRanks = np.zeros(Npop)
    # sort the array, then create an array of ranks
    sortedIndexes = scores.argsort()    
    populationRanks[sortedIndexes] = np.arange(Npop)

    # the inverse of the fitness rank
    # return Npop - populationRanks
    return populationRanks


def _rankFitnessInverted(scores, Npop):
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

