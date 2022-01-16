# -*- coding: utf-8 -*-
"""
TODO:
    The scheme is a little awkward right now, in that functions are passed
    arguements that they don't need.
    
    We could pass in the genePool to each sub-function. That would be more
    clean conceptually, but require that more genes are used.
    
    
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

def _mutateRandom(geneToMutate, randomGene, threshold, Pvector, N):
    """
    Randomly mutates a old gene to a new one.
    
    """
    newGene = np.zeros(N)
    
    # Find values to be mutated, assign them values from the random gene.
    mutateIndexes = np.where(Pvector < threshold)
    newGene[mutateIndexes] = randomGene[mutateIndexes]
    
    # pass the unmutated gene material
    mask = np.ones(N, np.bool)
    mask[mutateIndexes] = 0
    newGene[mask] = geneToMutate[mask]
    
    return newGene



def mutateRandom(geneToMutate, randomGene, threshold, bounds):
    """
    Randomly mutates the parts of a gene to other values that are also valid.

    Parameters
    ----------
    geneToMutate : gene
        The gene to mutate.
    randomGene : TYPE
        The a random gene with values that the old gene will be mutated to.
        This gene should be a valid solution as well.
    threshold : float
        The probaility each gene is mutated.
    bounds : flaot
        The bounds each gene is contained by. Unused by this function.

    Returns
    -------
    newGene : gene (1D numpy array).
        The mutated Gene.
    """
    
    # for each value we randomly mutate depeding on the threshold.
    N = len(geneToMutate)
    Pvector = getMutationChance(N)
    return _mutateRandom(geneToMutate, randomGene, threshold, Pvector, N)
    

# =============================================================================
# 
# =============================================================================
"""
TODO:
    This needs to be tested, specifically the part that enforces the boundary 
    conditions.
"""


def _getPerturbation(N, p):
    """
    Makes a vector that will scale the input up or down within
    """
    return np.ones(N) + np.random.uniform(-1,1,N)*p
    
    
def _mutatePerturbate(geneToMutate, threshold, Pvector, N, purtThreshold):
    """
    A mutation strategy where the values are slightly perturbed.
    Seperate function is used to enfore the bounary terms ion case we perturbe
    the function outside the initial bounds.
    """
    newGene = np.zeros(N)    
    # Find the values that were mutated, assign them values form the new gene.
    mutateIndexes = np.where(Pvector < threshold)
    Nmutate = len(mutateIndexes)
    
    perturbation = _getPerturbation(Nmutate, purtThreshold)
    newGene[mutateIndexes] = geneToMutate[mutateIndexes]*perturbation
    
    # Enforce Boundaries    
    
    # pass the unmutated gene material
    mask = np.ones(N, np.bool)
    mask[mutateIndexes] = 0
    newGene[mask] = geneToMutate[mask]
    
    return newGene


def _enforceBoundary(newGene, bounds):
    underInd = np.where(newGene < bounds[0]) 
    overInd  = np.where(bounds[1] < newGene)
    newGene[underInd] = bounds[0][underInd]
    newGene[overInd]  = bounds[1][overInd]
    return newGene


def mutatePerturbate(geneToMutate, randomGene, threshold, bounds, 
                     percent = 0.1):
    """
    Randomly mutates to a new gene that is also within the gene bounds, by
    changing it within a percentage of it's current value.
    
    Parameters
    ----------
    geneToMutate : gene (1d numpy array)
        The gene to be mutated.
    randomGene : gene (1d numpy array)
        A temporary gene. Unused by this function
    threshold : float
        The probability of a mutation occuring for each item in the list.
    bounds : flaot
        The bounds each gene is contained by. Unused by this function.
    percent : TYPE, optional
        The maximum mamount each gene will be perturbed by. The default is 0.1.

    Returns
    -------
    newGene : gene (1D numpy array).
        The mutated Gene.

    """
    # for each value we randomly mutate depeding on the threshold.
    N = len(geneToMutate)
    Pvector = getMutationChance(N)

    newGene =  _mutatePerturbate(geneToMutate, threshold, Pvector, N, percent)
    
    # Enforce Boundary Conditons
    newGene = _enforceBoundary(newGene, bounds)
    
    return newGene
    
