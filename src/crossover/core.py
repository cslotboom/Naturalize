# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""

import numpy as np
from ..solutionClass import Individual
from .strategies import crossGeneAvg, crossGeneSingleCut




def _parseStrategyInputs(strategy):
    """
    Parses the inputs. If a integer is passed in, we sleect the appropriate
    strategy. Otherwise we pass in the custom strategy directly
    """
    crossoverStrategies = {0:crossGeneSingleCut,
                           1:crossGeneAvg}
    
    
    if isinstance(strategy, int):
        if strategy not in crossoverStrategies.keys():
            raise Exception('Invalid strategy Index Provided')
        crossoverStrategy = crossoverStrategies[strategy]
    
    elif callable(strategy):
        crossoverStrategy = strategy
        
    return crossoverStrategy
        
        
def getCrossover(strategy = 0):
    """
    
    A functions that returns the desired crossover function/ It is possible to
    choose from a set of predefined functions, or using a custom function.
    
    When chosing from predefined functions, an integer is passed 
    
    Custom crossover functions will take in two lists, and return two ouput
    lists for each gene.
        f(geneA, geneB)  ->  newGeneA, newGeneB
    
    
    Parameters
    ----------
    crossoverStrategy : int, optional, or function
        The cross over strategy to use. The current strategies supported are        
        0: crossGeneSingleCut
        1: crossGeneSingleCutAvg
        
        The default is crossGeneSingleCut.

    Returns
    -------
    crossGenotypes: function
        the function used to cross genes.

    """

    crossoverStrategy = _parseStrategyInputs(strategy)
    
    
    def crossGenotypes(a: Individual, b: Individual):
        """
        Crosses over the geontypes of two individuals using the defined 
        strategies.

        Parameters
        ----------
        a : Individual
            The first individual.
        b : Individual
            The first individual.

        Returns
        -------
        tuple
            A tuple with the two new individuals in it.

        """
        genotypea = a.genotype
        genotypeb = b.genotype
        Ngenes = a.Ngenes
        
        aOut = [None]*Ngenes
        bOut = [None]*Ngenes        
        
        for ii in range(Ngenes):
            aOut[ii], bOut[ii] = crossoverStrategy(genotypea[ii], genotypeb[ii])
            
        return (Individual(aOut), Individual(bOut))    
    
    return crossGenotypes



# =============================================================================
# The same structure but using a class
# =============================================================================



# class Crossover:
    
#     def __init__(self, crossoverStrategy = crossGeneSingeCut):
#         self.cross = crossoverStrategy
        
        
#     def crossGenotypes(self, a: Individual, b: Individual):
#         genotypea = a.genotype
#         genotypeb = b.genotype
#         Ngenes = a.Ngenes
        
#         aOut = [None]*Ngenes
#         bOut = [None]*Ngenes        
        
#         for ii in range(Ngenes):
#             aOut[ii], bOut[ii] = crossGeneSingeCut(genotypea[ii], genotypeb[ii])
            
#         return (Individual(aOut), Individual(bOut))    
    