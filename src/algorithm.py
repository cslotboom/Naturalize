# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""


import numpy as np
from .solutionClass import Individual, Generation, DefaultGenePool

from .defaultFuncs import (initPopulation, defaultEnvironment, 
                           defaultCrossover, defaultMutate, 
                           defaultFitnessProbs, pick_Individual, 
                           namePopulation)
import pickle 


class AlgorithmHelper:
    """ 
    This class takes in the custom functions we define then passes it to the 
    genetic algorithm class
    """
    
    def __init__(self, ftest, ffit, 
                 genePool = DefaultGenePool,   
                 fmut = defaultMutate, 
                 fcross = defaultCrossover, 
                 fprobs = defaultFitnessProbs,
                 environment = defaultEnvironment()):
        
        self.ftest = ftest
        self.ffit = ffit
        self.fmut = fmut
        self.fcross = fcross
        
        self.getfitnessProbs = fprobs
        self.genePool = genePool
        
        self.environment = environment

class GeneticAlgorithm:
    
    def __init__(self, Helper, Ngen, Npopulation, Ncouples, Nsurvive, mutateThresold
                 ,recordGenerations = True):
        """
        The test is where the indivdual passes through the environment.
        This will lead to some raw result.
        The fitness function is then used to process the raw result and get
        the scalar fitness quantity.
        
        TODO: consider combining both functions into one.
        We could combine both into one function if we'd like.
        
        That is then. For many problems

        Parameters
        ----------
        Helper : TYPE
            DESCRIPTION.
        Ngen : TYPE
            DESCRIPTION.
        Npopulation : TYPE
            DESCRIPTION.
        Ncouples : TYPE
            DESCRIPTION.
        Nsurvive : TYPE
            DESCRIPTION.
        mutateThresold : TYPE
            DESCRIPTION.
        recordGenerations : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        


        # Optimization parameters
        self.Ngen = Ngen
        self.Npopulation = Npopulation
        self.Ncouples = Ncouples
        self.Nsurvive = Nsurvive
        self.mutateThresold = mutateThresold   
        
        
        # Record each generation if the user wants
        self.recordGens = recordGenerations
        if recordGenerations == True:
            self.gens = [None]*Ngen
        
        # Parameters for recording the prior and current best
        self.CurrentBest = None
        self.BestValues = np.zeros(Ngen)
        
        
        # Assign the key functions
        self.genePool = Helper.genePool
        self.test = Helper.ftest
        self.fitness = Helper.ffit
        self.cross = Helper.fcross
        self.mutate = Helper.fmut
        self.getfitnessProbs = Helper.getfitnessProbs
        self.environment = Helper.environment
        # Assign GenePool?

        self.best = None

    def getChild(self, population, fitnessProbs):
        """
        Gets the childeren of a single pair of individuals
        """
        mate1 = pick_Individual(population, fitnessProbs)
        mate2 = pick_Individual(population, fitnessProbs)
            
        child1, child2 = self.cross(mate1, mate2)
        child1 = self.mutate(child1, self.mutateThresold, self.genePool)
        child2 = self.mutate(child2, self.mutateThresold, self.genePool)
        
        return [child1, child2]
        
    def getOffspring(self, population, fitnessProbs):
        """
        Gets all of the childeren for an entire population.
        """        
        Offspring = []
        for jj in range(self.Ncouples):  
            Offspring += self.getChild(population, fitnessProbs)
            
        return Offspring
        
    def getSurvivers(self, population, fitnessProbs):
        """
        Chooses surviving members.
        """
        
        survivors = []
        for jj in range(self.Nsurvive):
            survivors += [pick_Individual(population, fitnessProbs)  ] 
            
        return survivors

    def addRandom(self, new_population):
        
        """
        Adds random individuals to a new population.
        """
        # add new random members
        while len(new_population) < self.Npopulation:
            newGenotype = self.genePool.getGenotype()
            new_population += [Individual(newGenotype)]
    

    def testGen(self, generation):
        
        """
        Tests all the individuals in the population
        """
        
        # Test individuals
        for individual in generation.population:
            #TODO: consider if it's better to change individual in funcition
            result = self.test(individual, self.environment)
            individual.result = result
            # print(result)
            
            
    def scoreGen(self, currentGen):
        
        # print(currentGen)
        self.testGen(currentGen)
        
        # Score Generation
        population = currentGen.population
        currentGen.scores = self.score_population(population)
        
        return currentGen.scores
    
    
    def score_population(self, population):
        # Find scores for every item of hte pupulation
        
        scores = []
        
        for ii in range(len(population)):
            score = self.fitness(population[ii], self.environment)
            scores += [score]
            
        return np.array(scores)    
    
    
    def checkIfBest(self, generation):
        """       
        Checks if the value is the best, stores it if it isn't
        """       
        
        
        if generation.bestScore <= self.currentBestScore:
            self.best = generation.best
            self.currentBestScore = generation.bestScore
        self.BestValues[generation.gen - 1] = self.currentBestScore 
        
        print('Current best score:', self.currentBestScore)    
        print('Current best genotype:', self.best.genotype)    
            
        
        
        
    def getNewGen(self, oldGeneration, genNumber):
        # Here we curate the population with some rules.
        # We first pick surviving genes by allowing the existing population to reproduce.
        # allow members of the population to reporuduce based on their relative score; 
        # i.e., if their score is higher they're more likely to reproduce
        
        scores = oldGeneration.scores
        fitnessProbs = oldGeneration.fitnessProbs
        population = oldGeneration.population
        ############################################################
    
        new_population = []
        new_population += self.getOffspring(population, fitnessProbs)
        new_population += self.getSurvivers(population, fitnessProbs)
            
        # add new random members to fill the rest of the population.
        self.addRandom(new_population)
            
        # #replace the old population with a real copy
        # # population = copy.deepcopy(new_population)
        # population = new_population
        new_generation = Generation(new_population, genNumber)
        
        namePopulation(new_population, genNumber)

        return new_generation

    
    def optimize(self):
        
        
        print('Generation 0')       
        gen = 0
        # Initialize the population 
        IntialPop = initPopulation(self.Npopulation, self.genePool)
        currentGen = Generation(IntialPop, gen)
                
        # Inialize the scores
        currentGen.scores = self.scoreGen(currentGen)
        currentGen.fitnessProbs = self.getfitnessProbs(currentGen.scores)
        self.currentBestScore = np.min(currentGen.scores)
        currentGen.recordBest()
        self.best = currentGen.best
        # self.checkIfBest(currentGen)

        for ii  in range(self.Ngen):
            print('Generation ', ii + 1)
           
            # Record the old generation
            if self.recordGens == True:
                self.gens[ii] = currentGen
            
            # Get the new generatation
            currentGen = self.getNewGen(currentGen, ii + 1)
            
            # Score the generation
            currentGen.scores = self.scoreGen(currentGen)
            currentGen.fitnessProbs = self.getfitnessProbs(currentGen.scores)
            
            # Record the best value int he current generation
            currentGen.recordBest()
            
            # Record the best values
            # self.recordBest(currentGen)
            self.checkIfBest(currentGen)
            
            # Record the current solution
            # currentBest = currentGen.best
            # print(currentGen.best.genotype)

            
        # Score final generation
        population = currentGen.population
        
        # print(currentGen.best.genotype)
        return currentGen.best
        
        
        
def pickleAnalysis(geneticAlgorithm, fileName):
    
    filehandler = open(fileName, 'wb')
    try:
        pickle.dump(geneticAlgorithm, filehandler)
    except:
        pass
    filehandler.close()
    
    
def readPickle(fileName):

    fileObj = open(fileName, 'rb')
    outputObject = pickle.load(fileObj)
    fileObj.close()

    return outputObject