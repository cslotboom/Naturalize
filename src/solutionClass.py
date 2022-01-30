# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""
import numpy as np
import random

from abc import ABC, abstractmethod

import collections
# =============================================================================
# Generation/Population
# =============================================================================


class Generation(collections.UserList):
    
    """ A generation contians a collection of all individuals in a population,
    As well as the score and rank of those individuals.
    
    Parameters
    ----------
    population : List
        A list of all the individuals in the current generation.
    genNumber : int
        The current generatio nnumber..

    """
    
    def __init__(self, population, genNumber):
        """
        Note, data is used to store the data that will be returned when using
        the "list-like" propreties of the generation.
        """
        self.data = population
        self.population = population
        self.size = len(population)
        
        self.gen = genNumber
        self.scores = [None]*self.size
        self.ranks = [None]*self.size
        self.best = None
    
    def getCurrentGenome(self):
        """
        Gets the genotypes of all individuals in a population.
        """
        
        Genome = [None]*self.size
        for ii, individual in enumerate(self.population):
            Genome[ii] = individual.genotype
            
        return Genome
    
    def setGenBest(self):
        """
        Sets the best individual in the population.

        """
        population = self.population
        scores = self.scores
    
        # Record current Best
        self.best = population[np.argmin(scores)]
        self.bestScore = scores[np.argmin(scores)]
        self.bestGenome = self.best.genotype           
    
    # def __getitem__(self, index):
    #     return self.Individuals[index]

# class GenTester():
#     def __init__(self, gen):
        
#         self.population = gen.population
        # self.population = []
        # self.size = gen.size
        
        # self.gen = gen.gen
        # self.scores = gen.scores
        # self.ranks = gen.ranks
        # self.best = gen.best

    # def getCurrentGenome(self):
    #     Genome = [None]*self.size
    #     for ii, individual in enumerate(self.population):
    #         Genome[ii] = individual.genotype
            
    #     return Genome
    
    # def recordBest(self):
    #     population = self.population
    #     scores = self.scores
    
    #     # Record current Best
    #     self.best = population[np.argmin(scores)]
    #     self.bestScore = scores[np.argmin(scores)]
    #     self.bestGenome = self.best.genotype   

def namePopulation(population, gen):
    """
    For each individual in the population, assign a name.
    """
    
    for ii, individual in enumerate(population):
        individual.name = int(ii)
        individual.gen = int(gen)

def initPopulation(size, genePool):
    """ Creates the first generation of the population"""
    gen = 0
    population = []
    for ii in range(size):
        genotype = genePool.getNewGenotype()
        population.append(Individual(genotype))
        
    namePopulation(population, gen)
        
    return population

# =============================================================================
# The default gene pool. The user may overwrite this with their own class
# =============================================================================

# TODO:
    # What restrictions exist on genes? Can they be any object?


# TODO:
    # Make the default genome a array of arrays.
#   Can the default genome be a list of list??


class Gene(np.ndarray):
    """
    all this will do is enforce the proper shape for a gene
    """
    # __init__(self,)

class Genotype():
    """
    This will ensure that goentypes have the proper structure.
    """





# class



class GenePool(ABC):

    @abstractmethod
    def getNewGenotype(self, rand, lbounds, ubounds):
        """
        The rule used to generate new genotypes.
        """





#TODO: FInd a wat o set genetype - sometimes we might only want integers, or
# a set

class BasicGenePool(GenePool):
    
    """
    The gene pool provides bounds on all possible genes. Genes are valid 
    solutions to the optimizatoin problem, and are either a int/float, 
    or numpy array. The gene pool also generates valid genes.
        
    This default gene pool selects valid solutions from a uniform distribution
    where any value can be selected between two different limits.
    
    llims and ulims is a list of the bounds on each genotype. These lists can
    be any objects that can be subtracted - typically this will be a float or 
    numpy array.
    
    It's also possible to provide one gene, generally a numpy array of floats. 
    In this case in this case that gene will be wrapped by a list.
    
    Parameters
    ----------
    llims : list, or float/int/np.array
        The lower bounds on each genes. 
    ulims : list, or float/int/np.array
        The upper bounds on each genes. 
    """
       
    # Generates valid solutions for each individual genom
    def __init__(self, llims, ulims):

        self.llims = self._validateGenotype(llims)
        self.ulims = self._validateGenotype(ulims)

    def _validateGenotype(self, limit):
        """
        Checks if the base item is a list, makes a list if not.
        Checks if the child items are lists, if so makes them np.arrays
        """
        
        # check if the input is a basic list, e.g. [1, 2, 4, 4.5]
        noList = True
        for ii in range(len(limit)):
            if hasattr(limit[ii], "__len__"):
                noList = False
        if noList:
            limit = np.array(limit)
        
        # Check if subitems are a lists - if so make the np.arrays.
        for ii in range(len(limit)):
            obj = limit[ii]
            if isinstance(obj, list):
                limit[ii] = np.array(obj)
                
        # Check if item itself is a list. If not, make it a list.
        if isinstance(limit, list) != True:
            limit = [limit]
                
        return limit
            
            
    def getNewGene(self, rand, lbounds, ubounds):
        """
        Randomly generates a gene between the upper and lower bounds based
        on a randomly generated number

        Parameters
        ----------
        rand : float 
            A number between 0 and 1. Used for linear interpolation between 
            geenes.
        lbounds : float/int/np.array
            The gene's lower bound.
        ubounds : float/int/np.array
            The gene's upper bound.

        Returns
        -------
        gene : TYPE
            DESCRIPTION.

        """
        dx = ubounds - lbounds
        gene = dx*rand + lbounds
        return gene
    
    def getNewGenotype(self):
        """
        Generates a new gene for each gene in the gene pool, then stores them 
        in the genotype list. 
        
        
        """
        Ngenes = len(self.llims)
        genotype = []
        for ii in range(Ngenes):
            lbounds = self.llims[ii]
            ubounds = self.ulims[ii]
            if not isinstance(lbounds, np.ndarray):
                Lgene = 1
            else:
                Lgene = len(lbounds)
            rand = np.random.random(Lgene)
            genotype.append(self.getNewGene(rand, lbounds, ubounds))
                        
        return genotype



class DynamicGenePool(GenePool):
    
    """
    The gene pool provides bounds on all possible genes. Genes are valid 
    solutions to the optimizatoin problem, and are either a int/float, 
    or numpy array. The gene pool also generates valid genes.
        
    This default gene pool selects valid solutions from a uniform distribution
    where any value can be selected between two different limits.
    
    llims and ulims is a list of the bounds on each genotype. These lists can
    be any objects that can be subtracted - typically this will be a float or 
    numpy array.
    
    It's also possible to provide one gene, generally a numpy array of floats. 
    In this case in this case that gene will be wrapped by a list.
    
    Parameters
    ----------
    llims : list, or float/int/np.array
        The lower bounds on each genes. 
    ulims : list, or float/int/np.array
        The upper bounds on each genes. 
    """
       
    # Generates valid solutions for each individual genom
    def __init__(self, llims, ulims, geneSizes):

        self.llims = self._validateGenotype(llims)
        self.ulims = self._validateGenotype(ulims)
        self.geneSizes = self._validateSizes()

    # def _validateGenotype(self, limit):
    #     """
    #     Checks if the base item is a list, makes a list if not.
    #     Checks if the child items are lists, if so makes them np.arrays
    #     """
        
    #     # check if the input is a basic list, e.g. [1, 2, 4, 4.5]
    #     noList = True
    #     for ii in range(len(limit)):
    #         if hasattr(limit[ii], "__len__"):
    #             noList = False
    #     if noList:
    #         limit = np.array(limit)
        
    #     # Check if subitems are a lists - if so make the np.arrays.
    #     for ii in range(len(limit)):
    #         obj = limit[ii]
    #         if isinstance(obj, list):
    #             limit[ii] = np.array(obj)
                
    #     # Check if item itself is a list. If not, make it a list.
    #     if isinstance(limit, list) != True:
    #         limit = [limit]
                
    #     return limit
            
            
    # def getNewGene(self, rand, lbounds, ubounds):
    #     """
    #     Randomly generates a gene between the upper and lower bounds based
    #     on a randomly generated number

    #     Parameters
    #     ----------
    #     rand : float 
    #         A number between 0 and 1. Used for linear interpolation between 
    #         geenes.
    #     lbounds : float/int/np.array
    #         The gene's lower bound.
    #     ubounds : float/int/np.array
    #         The gene's upper bound.

    #     Returns
    #     -------
    #     gene : TYPE
    #         DESCRIPTION.

    #     """
    #     dx = ubounds - lbounds
    #     gene = dx*rand + lbounds
    #     return gene
    
    # def getNewGenotype(self):
    #     """
    #     Generates a new gene for each gene in the gene pool, then stores them 
    #     in the genotype list. 
        
        
    #     """
    #     Ngenes = len(self.llims)
    #     genotype = []
    #     for ii in range(Ngenes):
    #         lbounds = self.llims[ii]
    #         ubounds = self.ulims[ii]
    #         if not isinstance(lbounds, np.ndarray):
    #             Lgene = 1
    #         else:
    #             Lgene = len(lbounds)
    #         rand = np.random.random(Lgene)
    #         genotype.append(self.getNewGene(rand, lbounds, ubounds))
                        
    #     return genotype









class SetGenePool(GenePool):
    
    """
    The set gene pool draws solutions from a set of input genes
        
    This default gene pool selects valid solutions from a uniform distribution
    where any value can be selected between two different limits.
    
    llims and ulims is a list of the bounds on each genotype. These lists can
    be any objects that can be subtracted - typically this will be a float or 
    numpy array.
    
    It's also possible to provide one gene, generally a numpy array of floats. 
    In this case in this case that gene will be wrapped by a list.
    
    Parameters
    ----------
    llims : list of sets, or set
        The sets solutions are to be drawn from. 
    """
       
    # Generates valid solutions for each individual genom
    def __init__(self, genotypes):
        self.sets = self._validateGenotype(genotypes)

    def _validateGenotype(self, genotypes):
        """
        Ensures the final solution is in the form [set1, set2, set3,..., setN]
        """
        
        # check if the input is a basic set
        if isinstance(genotypes, list):
            genotypes = [genotypes]
                        
        for ii, gene in enumerate(genotypes):
            GeneIsSet = isinstance(gene, set)
            if not GeneIsSet:
                raise Exception(f'Gene {ii+1} is not a set, all genes must be a set.')
        return genotypes
            
    def getNewGene(self, setIn, size):
        """
        Randomly generates a gene using the set and gene size

        Parameters
        ----------
        rand : float 
            A number between 0 and 1. Used for linear interpolation between 
            geenes.
        lbounds : float/int/np.array
            The gene's lower bound.
        ubounds : float/int/np.array
            The gene's upper bound.

        Returns
        -------
        gene : TYPE
            DESCRIPTION.

        """
        return random.sample(setIn, size)
    
    def getNewGenotype(self):
        """
        Generates a new gene for each gene in the gene pool, then stores them 
        in the genotype list. 
        
        
        """
        Ngenes = len(self.sets)
        genotype = []
        for ii in range(Ngenes):
            genotype.append(self.getNewGene(self.sets[ii], self.sizes[ii]))
        return genotype





# =============================================================================
# 
# =============================================================================

class Individual:
    """ 
    Stores the a genotype as well as some meta information about analysis. 
    This includes a name and a generation number.
    It also includes a result, which has the output of each individual when
    tests.
    """
    
    def __init__(self, genotype):
        self.genotype = genotype
        self.Ngenes = len(genotype)
        self.result = None
        
    def setname(self, name):
        self.name = name
    
    def setGen(self, gen):
        self.gen = gen

