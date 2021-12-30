# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian


"""

import numpy as np

def getMutationChance(N):
    """
    Returns the probability each gene is mutated
    """
    
    return np.random.random_sample(N)

# =============================================================================
# 
# =============================================================================

def _mutateRandom(oldGene, tempGene, threshold, Pvector, N):
    """
    A crossover startegy where the two genes are swapped beyond the cut line.
    
        abcde    =>    abCDE
        ABCDE          ABcde    
    """
    newGene = np.zeros(N)
    
    # Find the values that were mutated, assign them values form the new gene.
    mutateIndexes = np.where(Pvector < threshold)
    newGene[mutateIndexes] = tempGene[mutateIndexes]
    
    # pass the unmutated gene material
    mask = np.ones(N, np.bool)
    mask[mutateIndexes] = 0
    newGene[mask] = oldGene[mask]
    
    return newGene



def mutateRandom(oldGene, tempGene, threshold, bounds):
    """
    Randomly mutates to a new gene that is also within the gene bounds.
    """
    
    # for each value we randomly mutate depeding on the threshold.
    N = len(oldGene)
    Pvector = getMutationChance(N)
    return _mutateRandom(oldGene, tempGene, threshold, Pvector, N)
    

# =============================================================================
# 
# =============================================================================



def _getPerturbation(N, p):
    """
    Makes a vector that will scale the input up or down within
    """
    return np.ones(N) + np.random.uniform(-1,1,N)*p
    
    
def _mutatePerturbate(oldGene, threshold, Pvector, N, purtThreshold):
    """
    A mutation strategy where the values are slightly perturbed
    """
    newGene = np.zeros(N)    
    # Find the values that were mutated, assign them values form the new gene.
    mutateIndexes = np.where(Pvector < threshold)
    Nmutate = len(mutateIndexes)
    
    perturbation = _getPerturbation(Nmutate, purtThreshold)
    newGene[mutateIndexes] = oldGene[mutateIndexes]*perturbation
    
    # Enforce Boundaries    
    
    # pass the unmutated gene material
    mask = np.ones(N, np.bool)
    mask[mutateIndexes] = 0
    newGene[mask] = oldGene[mask]
    
    return newGene


def _enforceBoundary(newGene, bounds):
    underInd = np.where(newGene < bounds[0]) 
    overInd  = np.where(bounds[1] < newGene)
    newGene[underInd] = bounds[0][underInd]
    newGene[overInd]  = bounds[1][overInd]
    return newGene


def mutatePerturbate(oldGene, tempGene, threshold, bounds, p = 0.1):
    """
    Randomly mutates to a new gene that is also within the gene bounds.
    """
    
    # for each value we randomly mutate depeding on the threshold.
    N = len(oldGene)
    Pvector = getMutationChance(N)

    newGene =  _mutatePerturbate(oldGene, threshold, Pvector, N, p)

    # Enforce Boundary Conditons    
    underInd = np.where(newGene < bounds[0]) 
    overInd  = np.where(bounds[1] < newGene)
    newGene[underInd] = bounds[0][underInd]
    newGene[overInd]  = bounds[1][overInd]
    
    return newGene
    
