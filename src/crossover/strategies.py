# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian


The 

"""

import numpy as np

def getRandomCutPoint(genea, geneb):
    # get the size of the gene
    Nunits = max(len(genea), len(geneb))
    
    # pick a random cut point
    cut = np.random.choice(np.arange(Nunits))
    return cut


def _crossGeneSingleCut(genea, geneb, cut):
    """
    A crossover startegy where the two genes are swapped beyond the cut line.
    
        abcde    =>    abCDE
        ABCDE          ABcde    
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
    genea : 1D array
        An 1D array/list of genes.
    geneb : 1D array
        An 1D array/list of genes.
    cut : int
        The index of the cut point

    Returns
    -------
    aOut : 1D array
        The output 1D array/list of for gene a.
    bOut : 1D array
        The output 1D array/list of for gene b.

    """
    cut = getRandomCutPoint(genea, geneb)
       
    return _crossGeneSingleCut(genea, geneb, cut)
    
    
def crossGeneAvg(genea, geneb, cutInd):
    """
    A crossover startegy where the two genes are averaged after a cut point
    
    12347    =>    12334
    54321          54334    
    
    Parameters
    ----------
    genea : 1D array
        An 1D array/list of genes.
    geneb : 1D array
        An 1D array/list of genes.
    cut : int
        The index of the cut point


    Returns
    -------
    aOut : 1D array
        The output 1D array/list of for gene a.
    bOut : 1D array
        The output 1D array/list of for gene b.

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
# A class structure. This may be better in the long run.
# =============================================================================

# class CrossSingle():
    
#     def __init__(self, genea, geneb):
#         self.genea = genea
#         self.geneb = geneb
    
    
#     def getRandomCutPoint(self):
#         """
        
    
#         """
        
#         # get the size of the gene
#         Nunits = max(len(self.genea), len(self.geneb))
        
#         # pick a random cut point
#         cut = np.random.choice(np.arange(Nunits))
#         return cut



