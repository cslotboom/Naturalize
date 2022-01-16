# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian

        The test is where the indivdual passes through the environment.
        This will lead to some raw result.
        The fitness function is then used to process the raw result and get
        the scalar fitness quantity.
                
        TODO:
            Consider making mutate affect ALL genes.
            The more genes that are added, the less likely an individual will
            stay the same.
            I guess that probably is true to nature..
        
        
        That is then. For many problems

# TODO: simplify the ftest formulentation with a decorator.


"""


import os
import numpy as np
from copy import deepcopy
from .solutionClass import (Individual, Generation, BasicGenePool, 
                            initPopulation, namePopulation)

from .fitness import (basicFitness,
                      getProbStrategy, pick_Individual, 
                           )
from .env import defaultEnvironment
from .crossover import getCrossover
from .mutate import getMutate

class AlgorithmHelper:
    
    """
    The algorithm helper contains all the functions used to define the 
    optimization analysis. The user can set customized functions to the 
    algorithm if they want to override default behaviour.
    
    Parameters
    ----------
    ftest : function
        The test function to use in the analysis. This is used to "test" each
        individual, passing it through the environment and recording the raw 
        result.
    ffit : function, optional
        A function used to further process the results of the test function.
        The outputs of this function are what are used ultimately used to 
        evaluate system fitness. The default is basicFitness, which uses the
        results of the test function with no processing.
    genePool : class, optional
        The genePool to be used in the problem. This defines the shape of each 
        gene, as well as the all possible solutions.
    fmut : function, optional
        The function to be used for mutating genes. The default function is is defaultMutate.
    fcross : function, optional
        The function used to crossover genes. The default is a crossover with
        a single cut at a randomly selected point. Different crossover strategies
        can be selected using the "getCrossover" function, or set as defined by
        users.
    fprobs : TYPE, optional
        This funciton is used to     
        The function used to assign the cumulative liklihood of being selected
        for a population. The default is defaultFitnessProbs.
    environment : TYPE, optional
        DESCRIPTION. The default is defaultEnvironment().

    Returns
    -------
    None.

    """
    
    def __init__(self, ftest, genePool, ffit = basicFitness, 
                 fmut = getMutate(), 
                 fcross = getCrossover(), 
                 fprobs = getProbStrategy(),
                 environment = defaultEnvironment()):
        
        self.ftest  = ftest
        self.ffit   = ffit
        self.fmut   = fmut
        self.fcross = fcross
        
        self.getfitnessProbs = fprobs
        self.genePool = genePool
        
        self.environment = environment




class GeneticAlgorithm:
    
    def __init__(self, Npop, Ncouples, Nsurvive, Helper:AlgorithmHelper, 
                 mutThresold = 0.1, recordGenerations = False):
        """
        Defines how the population of solutions will change from generation 
        to generation. 


        Parameters
        ----------
        Helper : object
            The helper object to use for the analysis.
        Npop : int
            The population to be considered.
        Ncouples : int
            The number of couples to be considered.
        Nsurvive : int
            The number of survivers to be considered. These reach the next
            generation unchanged.
        mutThresold : float
            The likilhood of a mutation occuring in each gene individual.
        recordGenerations : boolean, optional
            A toggle that turns on or off the storing of generations. 
            The default is True, which stores all generations

        """

        # Optimization parameters
        # self.Ngen = Ngen
        self.Npop = Npop
        self.Ncouples = Ncouples
        self.Nsurvive = Nsurvive
        self.mutThresold = mutThresold
                
        # Record each generation if the user wants
        self.recordGens = recordGenerations       
        
        # if Helper == None:
        #     Helper = AlgorithmHelper()
        # Assign the key functions
        self.genePool = Helper.genePool
        self.ftest = Helper.ftest
        self.fitness = Helper.ffit
        self.cross = Helper.fcross
        self.mutate = Helper.fmut
        self.getfitnessProbs = Helper.getfitnessProbs
        self.environment = Helper.environment
        # Assign GenePool?
        self.best = None

    def getChild(self, population, fitnessProbs):
        """
        Gets the childeren of a single pair of individuals, using the rules
        defined 
        """
        mate1 = pick_Individual(population, fitnessProbs)
        mate2 = pick_Individual(population, fitnessProbs)
            
        child1, child2 = self.cross(mate1, mate2)
        child1 = self.mutate(child1, self.mutThresold, self.genePool)
        child2 = self.mutate(child2, self.mutThresold, self.genePool)
        
        return [child1, child2]
        
    def getOffspring(self, population, fitnessProbs):
        """
        Gets all of the childeren for an entire population.
        """        
        Offspring = []
        for jj in range(self.Ncouples):  
            Offspring += self.getChild(population, fitnessProbs)
            
        return Offspring
        
    def getSurvivers(self, population, fitnessProbs, scores):
        """
        Chooses surviving members.
        """
        
        # survivors = []
        # for jj in range(self.Nsurvive):
        #     survivors += [pick_Individual(population, fitnessProbs)]
        
        Index = scores.argsort()[:self.Nsurvive]
        pop = np.array(population)
        survivors = pop[Index]
            
        return list(survivors)

    def addRandom(self, new_population):
        
        """
        Adds random individuals to a new population.
        """
        # add new random members
        ii = len(new_population)
        # while len(new_population) < self.Npop:
        while ii < self.Npop:
            newGenotype = self.genePool.getNewGenotype()
            new_population += [Individual(newGenotype)]
            ii +=1
    def testGen(self, generation):
        
        """
        Tests all the individuals in the population
        """
        # Test individuals
        for individual in generation.population:
            
            individual.result = self.ftest(individual, self.environment)

            
    def scoreGen(self, currentGen):
        
        # print(currentGen)
        self.testGen(currentGen)
        
        # Score Generation
        population = currentGen.population
        currentGen.scores = self.score_population(population)
        
        return currentGen.scores
    
    def score_population(self, population):
        # Find scores for every item of hte pupulation
        
        scores = np.zeros(len(population))
        for ii in range(len(population)):
            # score = self.fitness(population[ii], self.environment)
            # scores += [score]     
      
            scores[ii] = self.fitness(population[ii], self.environment)
            if scores[ii] == 1.:
                pause = True      
            
        return scores   

    def initPopulation(self):
        
        return initPopulation(self.Npop, self.genePool)

def getNextGen(analysis, oldGeneration, genNumber):
    # Here we curate the population with some rules.
    # We first pick surviving genes by allowing the existing population to reproduce.
    # allow members of the population to reporuduce based on their relative score; 
    # i.e., if their score is higher they're more likely to reproduce
    
    scores = oldGeneration.scores
    fitnessProbs = oldGeneration.fitnessProbs
    population = oldGeneration.population
    ############################################################

    new_population = []
    new_population += analysis.getOffspring(population, fitnessProbs)
    new_population += analysis.getSurvivers(population, fitnessProbs, scores)
        
    # add new random members to fill the rest of the population.
    analysis.addRandom(new_population)
        
    # #replace the old population with a real copy
    # # population = copy.deepcopy(new_population)
    # population = new_population
    new_generation = Generation(new_population, genNumber)
    
    namePopulation(new_population, genNumber)

    return new_generation


# =============================================================================
# 
# =============================================================================


class Analysis():
    
    def __init__(self, algorithm:GeneticAlgorithm, recorder=None, printStatus=True):
   
        self.algorithm = algorithm
        self.recorder = recorder
        self.printStatus = printStatus
        
        self.genCount = 0
        self.currentGen = None
        self.currentBest = None
        
        if algorithm.ftest == None:
            raise Exception('No test function assigned to the algorithm.')
    
    def getCurretGen(self):
        return self.currentGen
    
    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm
    
    
    def scoreCurrentGen(self):
        #TODO: this may be slow
        
        currentGen =  self.currentGen
        
        # Inialize the scores
        # currentGen.scores = self.algorithm.scoreGen(currentGen)
        self.algorithm.scoreGen(currentGen)
        currentGen.fitnessProbs = self.algorithm.getfitnessProbs(currentGen.scores)
        
        # Record the best value int the current generation
        currentGen.setGenBest()
        self.currentBest = currentGen.best.genotype
        
    def initGeneration(self):
        """
        makes the first genreration
        
        """
        if self.printStatus == True:
            print('Generation 0')       
        gen = 0

        IntialPop = self.algorithm.initPopulation()
        self.currentGen = Generation(IntialPop, gen)
        self.scoreCurrentGen()
        # self.initRecorder()
        
        # Set the current generation and best score
        # self.currentGen = currentGen
        self.currentBestScore = np.min(self.currentGen.scores)
        
        
    def record(self):
        """
        If there is a recorder active, record an instance of the current
        generation.
        subtract 1 beccause the first generation is zero.
        """
        if self.recorder != None:
            self.recorder.record(self.currentGen)
            # print(self.currentGen.gen)
    
    
    def runAnalysis(self, Ngen, initialGen = None):
        
        """
        Record logic - record the veryt first generation. Then record every
        the other generations after, according to user defined rules.
        
        TODO:
            need some error handeling
        """
        
        # Intialize variables
        self.Ngen = Ngen
        
        # If it's the first generation, and no generation is supplied, make one.
        if self.genCount == 0 and initialGen == None:
            self.initGeneration()
            self.record()
        elif initialGen != None:
            self.currentGen = initialGen
            self.genCount = initialGen.gen #TODO: change variable name!
            
        for ii in range(self.Ngen):
            
            # if ii == 99:
            #     a = 1
            
            self.genCount += 1
            newGen = self.getNextGen()            
            self.analyzeGeneration(newGen)
            
            # we already have recordered the first generation!
            if self.genCount != 0:
                self.record()
        
        return self._smartReturn()
        
    def _checkGenSize(self, initialGen):
        if len(self.currentGen) != len(initialGen):
            raise Exception('New generation has different size than old generation.')
        
    
    def _smartReturn(self):
        """
        If the the genotype is trivial (only one gene), then we return an array
        of that gene only.
        """
        if len(self.currentBest) == 1:
            return self.currentBest[0]
        return self.currentBest
        
    
    
    def analyzeGeneration(self, newGen):
        
        
        if self.printStatus:
            print(f'Generation {self.genCount}')
               
        # Score the generation
        # self.algorithm.scoreGen(currentGen)
        newGen.scores = self.algorithm.scoreGen(newGen)
        newGen.fitnessProbs = self.algorithm.getfitnessProbs(newGen.scores)
        newGen.setGenBest()
        
        self.currentGen = newGen       
        self.currentBest = newGen.best.genotype
        
        
    def getNextGen(self):
        # Here we curate the population with some rules.
        # We first pick surviving genes by allowing the existing population to reproduce.
        # allow members of the population to reporuduce based on their relative score; 
        # i.e., if their score is higher they're more likely to reproduce
        
        oldGeneration = self.currentGen
        genNumber = self.genCount
        algorithm  = self.algorithm
        
        scores = oldGeneration.scores
        fitnessProbs = oldGeneration.fitnessProbs
        population = oldGeneration.population
        ############################################################
    
        new_population = []
        new_population += algorithm.getOffspring(population, fitnessProbs)
        new_population += algorithm.getSurvivers(population, fitnessProbs, scores)
            
        # add new random members to fill the rest of the population.
        algorithm.addRandom(new_population)
            
        # #replace the old population with a real copy
        new_generation = Generation(new_population, genNumber)
        
        namePopulation(new_population, genNumber)
    
        return new_generation        
        
    
    def getRecorderData(self):
        """ Fixe the data for processing, then return it."""
        myContainer = deepcopy(self.recorder)
        myContainer.data.convert()
        return myContainer.data
    
        
def SaveGeneration():
    pass
    
def loadGeneraton():
    pass



        # self.currentGen = currentGen
        # self.currentBest = currentGen.best






