# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian


"""

import numpy as np


# =============================================================================
# Single cut crossover
# =============================================================================

def getRandomCutPoint(genea, geneb):
    """
    Gets the index of a random cut point within the gene.

    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array of genes.
    geneb : 1D numpy array
        An 1D numpy array of genes.

    Returns
    -------
    cut : cutInd
        The Index where the cut betweent he two genes takes place.

    """
    # get the size of the gene
    Nunits = max(len(genea), len(geneb))
    
    # pick a random cut point
    cutInd = np.random.choice(np.arange(Nunits))
    return cutInd

def _crossGeneSingleCut(genea, geneb, cut):
    """
    A crossover startegy where the two genes are swapped beyond the cut line.
    The function is seperated from the randomly generated cut for testing 
    purposes

        abcde    =>    abCDE
        ABCDE    =>    ABcde    
    """
    # Concetenate makes a new object, no need for copies.
    aOut = np.concatenate([genea[:cut], geneb[cut:]])
    bOut = np.concatenate([geneb[:cut], genea[cut:]])
    
    return aOut, bOut

def crossGeneSingleCut(genea, geneb):
    """
    A crossover startegy where the two genes are swapped beyond the cut line.
    
        abcde    =>    abCDE
        ABCDE          ABcde    

    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array/list of genes.
    geneb : 1D numpy array
        An 1D numpy array/list of genes.
    cut : int
        The index of the cut point

    Returns
    -------
    aOut : 1D numpy array
        The output 1D numpy array/list of for gene a.
    bOut : 1D numpy array
        The output 1D numpy array/list of for gene b.

    """
    cut = getRandomCutPoint(genea, geneb)
       
    return _crossGeneSingleCut(genea, geneb, cut)
    

# =============================================================================
# Average crossover.
# =============================================================================
    
def crossGeneAvg(genea, geneb):
    """
    A crossover startegy where the two genes are averaged, with no cut point
    
    12347    =>    33334
    54321          33334    
    
    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array of genes.
    geneb : 1D numpy array
        An 1D numpy array of genes.

    Returns
    -------
    aOut : 1D numpy array
        The output 1D numpy array/list of for gene a.
    bOut : 1D numpy array
        The output 1D numpy array/list of for gene b.

    """    
    
    avg = np.average([geneb,genea],0)
    aOut = avg
    bOut = avg
    
    return aOut, bOut



# =============================================================================
# random Crossover single cut crossover.
# =============================================================================
  
def crossGeneSingleCutAvg(genea, geneb, cutInd):
    """
    A crossover startegy where the two genes are averaged after a cut point
    
    12347    =>    12334
    54321          54334    
    
    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array/list of genes.
    geneb : 1D numpy array
        An 1D numpy array/list of genes.
    cut : int
        The index of the cut point


    Returns
    -------
    aOut : 1D numpy array
        The output 1D numpy array/list of for gene a.
    bOut : 1D numpy array
        The output 1D numpy array/list of for gene b.

    """    
    
    cut = getRandomCutPoint(genea, geneb)
           
    return _crossGeneSingleCut(genea, geneb, cut)

def _crossGeneAvgSingleCut(genea, geneb, cut):
    """
    A crossover startegy where the two genes are averaged after a cut point
    
    12347    =>    12334
    54321          54334    
    
    """
    # Concetenate makes a new object, no need for copies.
    avg = np.average([geneb[cut:],genea[cut:]],0)
    aOut = np.concatenate([genea[:cut], avg])
    bOut = np.concatenate([geneb[:cut], avg])
    
    return aOut, bOut



# =============================================================================
# Random cut Crossover
# =============================================================================
  


def _getRandomCrosInd(genea, geneb):
    """
    Swaps the genetic information of genes at random points

    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array/list of genes.
    geneb : 1D numpy array
        An 1D numpy array/list of genes.

    Returns
    -------
    cut : cutInd
        The Index where the cut betweent he two genes takes place.

    """
    
    
    # get the size of the gene
    Nunits = min(len(genea), len(geneb))
    
    # pick a random cut point
    Ncross = np.random.choice(np.arange(Nunits))
    
    # randomly select a number of items 
    crossInds = np.random.choice(np.arange(Nunits), Ncross, False)
    return crossInds



def crossGeneRandom(genea, geneb):
    """
    A crossover startegy where parts of two genes are randomly swapped.
    
    12347    =>    14341
    54321          52327    
    
    Parameters
    ----------
    genea : 1D numpy array
        An 1D numpy array/list of genes.
    geneb : 1D numpy array
        An 1D numpy array/list of genes.


    Returns
    -------
    aOut : 1D numpy array
        The output 1D numpy array/list of for gene a.
    bOut : 1D numpy array
        The output 1D numpy array/list of for gene b.

    """    
    
    crossInds = getRandomCutPoint(genea, geneb)
           
    return _crossGeneSingleCut(genea, geneb, crossInds)

def _crossGeneRandom(genea, geneb, crossInds):
    """
    A crossover startegy where parts of two genes are randomly swapped.
    
    12347    =>    14341
    54321          52327    
    
    """
    # Be careful with copying here.
    
    aOut = genea
    aOut[crossInds] = geneb[crossInds]
    bOut = geneb
    bOut[crossInds] = genea[crossInds]
    
    return aOut, bOut


