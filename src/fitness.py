# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian

"""

import numpy as np
from .solutionClass import Individual


# =============================================================================
# Fitness functions
# =============================================================================

def basicFitness(individual, env):
    """ 
    The trivial case, where fitness is just the result of passing through
    the environment.
    """       
    
    return individual.result

# =============================================================================
# Rank populations
# =============================================================================
"""
Thes functions are used to rank the score of individuals within a population.
"""

def rankFitness(scores, Npop):
    """
    Assign a rank to each item in the population, with low scores being 
    assigned the first rank.
    
      [0, 1, 100, 20, 0.1, 5]   - >    [0, 2, 5, 4, 1, 3]
    
    Parameters
    ----------
    scores : list
        A list of input scores input scores.
    Npop : int
        THe number of individuals in the population.

    Returns
    -------
    float
        The ranks in order of lowest output to highest output.    
    
    """
    populationRanks = np.zeros(Npop)

    # sort the array, then create an array of ranks
    sortedIndexes = scores.argsort()    
    populationRanks[sortedIndexes] = np.arange(Npop)
    return populationRanks

def rankFitnessInversed(scores, Npop):
    """
    Assign a rank to each item in the population, with high scores being assigned
    the highest rank.
    
      [0, 1, 100, 20, 0.1, 5]   - >    [5, 3, 0, 1, 4, 2]
      
    Parameters
    ----------
    scores : list
        A list of input scores input scores.
    Npop : int
        THe number of individuals in the population.

    Returns
    -------
    float
        The ranks in order of highest output to lowest output.

    """
          
    ranks = rankFitness(scores, Npop)
    return Npop - ranks





# =============================================================================
# 
# =============================================================================

"""
Ranked Fitness probabilities
Defines the probability that a parent is chosen.

probabilities are represented as a cumulative distrtibution 
Defines the likilhood a gene is chosen for reproduction. The input scores
can have any positive values.
    Each point in the output array has width equal to the liklihood of it being
    chosen.   
"""

def _parseStrategyInputs(strategy):
    """
    Parses the inputs. If a integer is passed in, we sleect the appropriate
    strategy. Otherwise we pass in the custom strategy directly
    """
    crossoverStrategies = {0:rankedRouletteFitnessProbs,
                           1:rouletteFitnessProbs,
                           }
    
    if isinstance(strategy, int):
        if strategy not in crossoverStrategies.keys():
            raise Exception('Invalid strategy Index Provided')
        crossoverStrategy = crossoverStrategies[strategy]
    
    elif callable(strategy):
        crossoverStrategy = strategy
        
    return crossoverStrategy
        
        
def getProbStrategy(strategy = 0):
    """
    
    A functions that returns the desired probability defintion function. It is 
    possible to choose from a set of predefined functions, or use a custom 
    function.
    
    When chosing from predefined functions, an integer is passed.
    
    Custom probability functions will returna  cumulative distribution for a 
    set of input individuals.

    Parameters
    ----------
    crossoverStrategy : int, optional, or function
        The cross over strategy to use. The current strategies supported are        
        0: rankedRouletteFitnessProbs
        1: rouletteFitnessProbs
        
        The default is rankedRouletteFitnessProbs.

    Returns
    -------
    probabilityFunction: function
        The function used to define the cumulative distribution for a set
        of scores in the population.
    """

    return _parseStrategyInputs(strategy)

    


def rankedRouletteFitnessProbs(scores):
    """
    Assigns probabilities of being chosen to a set of scores, based on the rank 
    of each score in the population.
    
    The probability of each selection is assigned with the goal of minimizing
    the input score.
    
    Parameters
    ----------
    scores : list
        The input fitness/score of each individual after it's passed through 
        the environment and processed by the fitness function.

    Returns
    -------
    probs : list
        The output cumulative distribution is for the scores.
        
    """

    Npop = len(scores) 
    populationRanks = rankFitness(scores, Npop)
    
    wheelAreas = Npop - populationRanks
    cumulativeFitness = np.cumsum(wheelAreas)
    probs = cumulativeFitness / cumulativeFitness[-1]
    
    return probs



def rouletteFitnessProbs(scores):
    """
    Assigns probabilities of being chosen to a set of scores, based on the 
    score of each individual in the population.
    
    The probability of each selection is assigned with the goal of minimizing
    the input score.
    
    Parameters
    ----------
    scores : list
        The input fitness/score of each individual after it's passed through 
        the environment and processed by the fitness function.

    Returns
    -------
    probs : list
        The output cumulative distribution is for the scores.
        
    """
    Npop = len(scores) 
    populationRanks = rankFitness(scores, Npop)
    
    wheelAreas = Npop - populationRanks
    cumulativeFitness = np.cumsum(wheelAreas)
    probs = cumulativeFitness / cumulativeFitness[-1]
    
    return probs

def pick_Individual(population, probs):
    """
    

    Parameters
    ----------
    population : list
        The input population of individuals.
    probs : array
        The cumulative probability distribution for the population.

    Returns
    -------
    selection : individual
        The selected individual from the population.

    """
    
    # Select a mamber of the pupulation at random depending on the ranked probability
    rand = np.random.random()
    selection = population[np.argmax(rand < probs)]
    return selection



