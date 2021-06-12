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
    
    def setGenBest(self):
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



# =============================================================================
# The default gene pool. The user may overwrite this with their own class
# =============================================================================

# TODO:
    # What restrictions exist on genes? Can they be any object?


# TODO:
    # Make the default genome a array of arrays.
#   Can the default genome be a list of list??



class GenePool:
    
    pass




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
        """
        llims and ulims is a list of the bounds on each gene.
        They support any objects that can be subtracted - Typically this will be
        a float or numpy array.
        
        llims and ulims alternatively can be a single numpy array.
        In this case it will be wrapped by a list.
        
        """
        # If the object isn't contained in a list
        # This makes input cleaner
        if isinstance(llims, list) != True:
            llims = [llims]
        if isinstance(ulims, list) != True:
            ulims = [ulims]
        else: 
            print(not isinstance(llims, list))

        
        self.llims = llims
        self.ulims = ulims

    def getGene(self, rand, lbounds, ubounds):
        
        dx = ubounds - lbounds
        gene = dx*rand + lbounds
        return gene
    
    def getGenotype(self):
        """
        Gets all genes and stores it in a container
        """
        
        Ngenes = len(self.llims)
        genotype = []
        for ii in range(Ngenes):
        
            lbounds = self.llims[ii]
            ubounds = self.ulims[ii]
            rand = np.random.random(Ngenes)
            genotype.append(self.getGene(rand, lbounds,ubounds ))
        
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
        
        # Check if 
        self.genotype = genotype
        self.Ngenes = len(genotype)
        self.result = None
        
    def setname(self, name):
        self.name = name
    
    def setGen(self, gen):
        self.gen = gen

