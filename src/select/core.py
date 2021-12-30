# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""

import numpy as np
from ..solutionClass import Individual
from .strategies import mutateRandom, mutatePerturbate




def _parseStrategyInputs(strategy):
    """
    Parses the inputs. If a integer is passed in, we select the appropriate
    strategy. Otherwise we pass in the custom strategy directly
    """
    crossoverStrategies = {0:mutateRandom,
                           1:mutatePerturbate}
    
    
    if isinstance(strategy, int):
        if strategy not in crossoverStrategies.keys():
            raise Exception('Invalid strategy Index provided')
        crossoverStrategy = crossoverStrategies[strategy]
    
    elif callable(strategy):
        crossoverStrategy = strategy
        
    return crossoverStrategy
        
        
def getMutate(strategy = 0, **kwargs):
    """
    
    A function that defines the desired mutation function. It is possible to
    choose from a set of predefined functions, or using a custom function.
    
    When chosing from predefined functions, an integer is passed to the function.
    When chosing a custion funciton, the funciton is passed in directly.
    
    Custom mutation functions will take in an individual, mutation threshold,
    and genePool, then return two ouputs.
    lists for each gene.
        f(Indivdual, mutThreshold, GenePool)  ->  mutated Individual
    
    
    Parameters
    ----------
    crossoverStrategy : int, optional, or function
        The cross over strategy to use. The current strategies supported are:      
        
        0 : mutateGeneRandom
            Randomly selects genes to change with a unifirom distribution.
            Changes the gene to a randomly selected value within the bounds.
        1 : mutateGenePerturbate
            Randomly selects genes to change with a uniform distribution.
            Changes mutated genes by a percentage of there current value.
            Requires addtional kwargs:
            
            p : float, optional 
                The percentage to change the value by. Has a default 
                value of 0.1.
        
        The default function is 'mutateGeneRandom'.

    Returns
    -------
    Function
        The mutation funciton to be used in the analysis.

    """

    mutateStrategy = _parseStrategyInputs(strategy)

    
    def mutateGenotypes(a: Individual, mutThreshold, GenePool):
        """
        Mutates each gene in the genotype of indivudal using the specified 
        strategy.

        Parameters
        ----------
        a : Individual
            The individual to mutate .
        mutThreshold : float in [0,1]
            The chance a mutation occurs in each gene.
        GenePool : Individual
            The gene pool used to select individuals.
        Returns
        -------
        Individual
            The mutated individual in the population.

        """
        
        
        genotypea = a.genotype
        Ngenes = a.Ngenes
        newGenotype = [None]*Ngenes
        tempGenotype = GenePool.getNewGenotype()        
        
        
        for ii in range(Ngenes):
            oldGene = genotypea[ii]
            tempGene    = tempGenotype[ii]
            bounds = [GenePool.llims[ii],  GenePool.ulims[ii]]
            newGenotype[ii] = mutateStrategy(oldGene, tempGene, mutThreshold, bounds, **kwargs)

        return Individual(newGenotype)
    
    return mutateGenotypes




# class Crossover:
    
#     def __init__(self, strategy, kwargs):
#         self.mutateStrategy  = _parseStrategyInputs(strategy)
        
        
#     def mutateGenotypes(self, a: Individual, mutThreshold, GenePool):
#         """
#         Mutates each gene in the genotype of indivudal using the specified 
#         strategy.

#         Parameters
#         ----------
#         a : Individual
#             The individual to mutate .
#         mutThreshold : float in [0,1]
#             The chance a mutation occurs in each gene.
#         GenePool : Individual
#             The gene pool used to select individuals.
#         Returns
#         -------
#         Individual
#             The mutated individual in the population.

#         """
        
        
#         genotypea = a.genotype
#         Ngenes = a.Ngenes
#         newGenotype = [None]*Ngenes
#         tempGenotype = GenePool.getNewGenotype()        
            
        
#         for ii in range(Ngenes):
#             oldGene = genotypea[ii]
#             tempGene    = tempGenotype[ii]
#             newGenotype[ii] = self.mutateStrategy(oldGene, tempGene, mutThreshold, **self.kwargs)

#         return Individual(newGenotype)



# def defaultMutate(individual, threshold, GenePool):
    
#     """
#     Mutate will randomly generate a new solution based on the old solution.
    
#     The default mutate function generates valid solutions where the solution
#     is an array of inputs:
#         X = [x1, x2, x3, ..., xN]
    
#     And, that array for two valid solutions X and Y, the solution Z is also a 
#     solution
#         Z = [y1, x2, x3, y4, ..., yN]
 
#     """   
    
#     # Given an individual, randomly create a new solution
#     Ngenes = len(individual.genotype)
#     newGenotype = [None]*Ngenes
#     tempGenotype = GenePool.getNewGenotype()
    
#     for ii in range(Ngenes):
#         oldGene = individual.genotype[ii]
#         tempGene    = tempGenotype[ii]
#         newGenotype[ii] = mutateGene(individual, oldGene, tempGene, threshold)

    
#     return Individual(newGenotype)


# =============================================================================
# The same structure but using a class
# =============================================================================




    