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
            Genome[ii] = individual.genome
            
        return Genome
    
    def recordBest(self):
        population = self.population
        scores = self.scores
    
        # Record current Best
        self.best = population[np.argmin(scores)]
        self.bestScore = scores[np.argmin(scores)]
        self.bestGenome = self.best.genome           
    
    # def __getitem__(self, index):
    #     return self.Individuals[index]

# =============================================================================
# The default gene pool. The user may overwrite this with their own class
# =============================================================================

# TODO:
    # What restrictions exist on genes? an they be any object

class DefaultGenePool:
    
    """
    The gene pool generates valid "genes" or solutions.
    
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
    
    def getGenome(self):
        Ngenes = len(self.llims)
        rand = np.random.random(Ngenes)
        genome = self.getGene(rand)
        
        return genome


# =============================================================================
# 
# =============================================================================

class Individual:
    """ Contains the genome and some other stuff.
    
    A genome is a valid solution in the solution space.
    Each will have a name and a generation number.
    
    The Individual will also have a result, which is the output of the test.
    """
    
    def __init__(self, genome):
        self.genome = genome
        self.result = None
        
    def setname(self, name):
        self.name = name
    
    def setGen(self, gen):
        self.gen = gen

