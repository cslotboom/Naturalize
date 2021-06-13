# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""


import forallpeople
import os
import numpy as np
from .solutionClass import Individual, Generation, DefaultGenePool

# from .defaultFuncs import (initPopulation, defaultEnvironment, 
#                            defaultCrossover, defaultMutate, 
#                            defaultFitnessProbs, pick_Individual, 
#                            namePopulation)
import pickle 

# from .



# The 
np.ndarray


"""
Get the cumulative best using another parser function
"""


class dataContainer:
    
    
    def __init__(self):
        
        """
        When recording we use lists because it is much quicker to append data
        to them.
        """
        
        self.bestIndivduals = []  # The best individual of the current generation
        self.bestGenotypes = []        
        self.bestScores  = []
        self.genNumber = []
        self.populations = []
        
    def getAvgScore(self,gen):
        
        pass

    def convert(self):
    
        """
        This might be a terrible terrible practice, but I'm testing it out because
        I'm brave.
        
        Convers all curent attributes to a np array.
        """
        for item in self.__dict__:
            if isinstance(self.__dict__[item], list):
                self.__dict__[item] = np.array(self.__dict__[item])
        
# test = dataContainer()
# for item in test.__dict__:
#     print(item)
#     print(test.__dict__[item])

class generationData():
    
    def __init__(self, population):
        pass        
    

# The recorder object should have rules for recording the current generation




class basicRecorder():
    
    
    def __init__(self, Nrecord: int, Nstore: int):
        
        self.data = dataContainer()
        
        self.Nrecord = Nrecord
        self.Nstore = Nstore
        
        self.genNumber = []
        
        # Parameters for recording the prior and current best
        self.bestIndivduals = []  # The best individual of the current generation
        self.bestGenotypes = []        
        self.bestScores  = []   # The best individual of the


        self.populations = []
        
        
        # self.avgbest = []

    def shouldRecord(self, N):
        """
        Checks if the current generation should be recorded.
        """
        
        if N% self.Nrecord ==0:
            return True
        return False


    def recordBestAbsolute(self, currentGen):
        """
        Records the single best geontype, individual and value
        """

        self.data.bestIndivduals.append(currentGen.best)
        self.data.bestGenotypes.append(currentGen.best.genotype)
        self.data.bestScores.append(currentGen.bestScore)


    def recordBestPool(self, currentGen):
        """
        Records the best Nstore individuals of the current generation in
        a population.
        """

        # Record a pool
        # Sort the indexes, keep the best Nstore of them        
        keepInexes  = np.argsort(currentGen.scores)[:self.Nstore]
        tempPop     = np.array(currentGen.population)
        
        storedIndividuals = tempPop[keepInexes]
        self.data.populations.append(storedIndividuals)
        
        

    def record(self, currentGen):
        
        if self.shouldRecord(currentGen.gen) == False:
            return
                    
        # Record the best of each generation
        self.data.genNumber.append(currentGen.gen)
        self.recordBestAbsolute(currentGen)
        self.recordBestPool(currentGen)

            
        
    def recordIfBest(self, generation):
        """       
        Checks if the best in the current generation is better than all priors 
        stores it if it is.
        """       

        
        if generation.bestScore <= self.currentBestScore:
            # If the current generation  is better, store the new best value
            self.currentBest = generation.best
            self.currentBestScore = generation.bestScore
            
            self.cumBestIndivduals[generation.gen - 1] = generation.best 
        
        # If it's the first generation, store the value no matter what.
        elif generation.gen == 0:
            self.cumBestIndivduals[generation.gen - 1] = generation.best
            
        # if the current score isn't bigger, store the old one.
        else:
            self.cumBestIndivduals[generation.gen - 1] = self.cumBestIndivduals[generation.gen - 2] 
        
        # Store the current best score.
        self.genBestScores[generation.gen - 1] = generation.bestScore
        self.cumBestScores[generation.gen - 1] = self.currentBestScore         
        
        
        
    # self.bestScores
    # self.avgScore


    ## Record
    # Record the best value int the current generation
    # currentGen.recordGenBest()
                
    # self.genBestIndivduals[self.currentGen] = currentGen.best
    
    # Record the best values
    # self.recordIfBest(currentGen)
    
    # Record the current solution
    # currentBest = currentGen.best
    # print(currentGen.best.genotype)
    
    # Update the generation
    
    # TODO: move print to recorder.
    # print('Current best score:', self.currentBestScore)    
    # print('Current best genotype:', self.currentBest.genotype)   




        # self.currentGen = currentGen
        # self.currentBest = currentGen.best





def _flattenGene(individual, Nunits):
    
    flatGene = [0]*Nunits
    ii = 0
    for gene in individual.genotype:
        for data in gene:
            flatGene[ii] = data
            ii+=1
            
    return np.array(flatGene)

def _geneToStr(gene):
    tmpStr = ''
    tempInt = len(gene)    
    for ii, item in enumerate(gene):
        tmpStr += str(item)
        if ii != tempInt - 1:
            tmpStr += ','
    tmpStr += '\n'
    return tmpStr


def _getTxtOut(genNumber, flatGenes, Lgenes):
    
    """
    Writes out the generation data as text.
    """
    
    lines = []
    header = f'Data from generation: {genNumber}\n'
    lines.append(header)
    lines.append('Gene Lengths:\n')
    
    header2 = []
    for ii, L in enumerate(Lgenes):
        header2.append(f'{L}')
    header2 = ','.join(header2)
    header2 += '\n'
    lines.append(header2)
    
    for gene in flatGenes:        
        lines += [_geneToStr(gene)]
    return lines


def saveCurrentGen(analysis, fileName):
    
    """
    Note, some rounding occurs when saving to .txt! THis may affect really sensetive
    results.
    """
    
    
    currentGen = analysis.currentGen
    
    population = currentGen.population
    genNumber  = currentGen.gen
    Npop = len(population)
    
    indv = population[0]
    Lgenes = []
    for gene in indv.genotype:
        Lgenes.append(len(gene))
        
    Nunits = np.sum(Lgenes)
    flatGenes = np.zeros((Npop, Nunits))
    
    for ii, indv in enumerate(population):
        flatGenes[ii] = _flattenGene(indv, Nunits)
    
    txtOut = _getTxtOut(genNumber, flatGenes, Lgenes)
    with open(fileName, "w") as output:
        output.writelines(txtOut)


def _getIndv(row, Lgenes):
    cutLow = 0
    cutHigh = 1
    genotype = []
    
    for L in Lgenes:
        cutHigh += L 
        gene = row[cutLow:cutHigh]
        cutLow  += L
        
        genotype.append(gene)
        
    return Individual(genotype)


def readSavedGen(FileName):
    
    header = np.loadtxt(FileName, str, max_rows = 3, delimiter =',')
    data = np.loadtxt(FileName, float, skiprows = 3, delimiter =',')
    
    headerLengths = 2
    Lgenes = np.array(header[headerLengths:], int)
    genNumber = int(header[0].split(': ')[1])
    
    
    population = []
    for row in data:        
        indv = _getIndv(row, Lgenes)
        population.append(indv)
    
    gen = Generation(population, genNumber)
    
    return gen
        
    
    
    
    
    
        
    
    # for ii in range()
        
    # Flatten Genes
    
    

# with open("file.txt", "w") as output:
#     output.write(str(values))




def pickleAnalysis(geneticAlgorithm, fileName):

    
    # Delete the old object
    if os.path.isfile(fileName):
        os.remove(fileName)
        print('Removing old file at: ', fileName)
    
    filehandler = open(fileName, 'wb')

    
    try:
        pickle.dump(geneticAlgorithm, filehandler)
        print('File Saved at: ', fileName)
    except:
        print('Saving Failed.')
        pass
    filehandler.close()
    
    
def readPickle(fileName):

    fileObj = open(fileName, 'rb')
    outputObject = None
    try:
        outputObject = pickle.load(fileObj)
        print('File Loaded at: ', fileName)
    except:
        print('Loading Failed.')
    
    fileObj.close()

    return outputObject


def SaveGeneration():
    pass
    
def loadGeneraton():
    pass