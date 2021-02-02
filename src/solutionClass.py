# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""
import numpy as np

# =============================================================================
# Generation/Population
# =============================================================================


class Generation:
    
    """ A generation contians a collection of all individuals in a population,
    As well as the score and rank of those individuals.
    """
    
    def __init__(self, population, genNumber):
        # self.size = size
        # a list of all the individuals in a generaiton
        self.population = population
        self.size = len(population)
        
        self.gen = genNumber
        self.scores = [None]*self.size
        self.ranks = [None]*self.size
        self.best = None
    
    def getCurrentGenome(self):
        Genome = [None]*self.size
        for ii, individual in enumerate(self.population):
            Genome[ii] = individual.genotype
            
        return Genome
    
    def recordBest(self):
        population = self.population
        scores = self.scores
    
        # Record current Best
        self.best = population[np.argmin(scores)]
        self.bestScore = scores[np.argmin(scores)]
        self.bestGenome = self.best.genotype           
    
    # def __getitem__(self, index):
    #     return self.Individuals[index]

# =============================================================================
# The default gene pool. The user may overwrite this with their own class
# =============================================================================

# TODO:
    # What restrictions exist on genes? an they be any object


# TODO:
    # Make the default genome a array of arrays.
#   Can the default genome be a list of list??


class DefaultGenePool:
    
    """
    The gene pool generates valid "genes" or solutions.
    
    A gene pool is a reflection of all current genes. It differes from the 
    environment in that the genes change through the analysis.
    
    The environment is static!
    Perhaps the methods of generating genes should be in the environment?
    
    This default gene pool selects valid solutions from a uniform distribution
    between two different limits.
       
    """
    
    # Generates valid solutions for each individual genom
    def __init__(self, llims, ulims):
        self.llims = llims
        self.ulims = ulims

    def getGene(self, rand):
        
        dx = self.ulims - self.llims
        gene = dx*rand + self.llims
        return gene
    
    def getGenotype(self):
        Ngenes = len(self.llims)
        rand = np.random.random(Ngenes)
        genotype = self.getGene(rand)
        
        return genotype


# =============================================================================
# 
# =============================================================================

class Individual:
    """ Contains the genotype and some other stuff.
    
    A genotype is a valid solution in the solution space.
    Each will have a name and a generation number.
    
    The Individual will also have a result, which is the output of the test.
    """
    
    def __init__(self, genotype):
        self.genotype = genotype
        self.result = None
        
    def setname(self, name):
        self.name = name
    
    def setGen(self, gen):
        self.gen = gen

