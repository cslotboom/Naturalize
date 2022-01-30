# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""
import forallpeople
import os
import numpy as np
from .solutionClass import Individual, Generation, BasicGenePool


import pickle 

"""
Get the cumulative best using another parser function
"""

"""
Many of the recoder classes directly reference attribures of the data container.
This seems like a bad practice.

I think the dataContainer class will remain relatively static though.
It's really just a suggestion for what we can record with the recorder.
Let's try leaving it for now and see what happens.'
"""

class dataContainer:
    
    
    def __init__(self, size = 1):
        # The best individual of the current generation
        self.bestIndividuals = []
        self.bestGenotypes = []    
        self.bestScores  = []
        self.genNumber = []
        self.populations = []
        self.populationBestScores = []
        
    def getAvgScore(self,gen):
        pass

    def convert(self):
    
        """
        This might be a terrible terrible practice, but I'm testing it out because
        I'm brave.
        Maybe instead of this I'll try "return converted".
        
        Convers all curent attributes to a np array.
        """
        for item in self.__dict__:
            if isinstance(self.__dict__[item], list):
                self.__dict__[item] = np.array(self.__dict__[item])

class generationData():
    
    def __init__(self, population):
        pass        
    
"""
This is tightly coupled to the individual object and generation objects
"""



class Recorder():
    
    def __init__(self, recordEvery:int, Nstore:int = 1, printStatus = True):






        self.recordEvery = recordEvery
        self.Nstore = Nstore   
        # consider removing this reference, and instead passing in the container
        self.data = dataContainer()
        self.printStatus = printStatus

    def shouldRecord(self, N):
        """
        Checks if the current generation should be recorded.
        """
        if (N)% self.recordEvery ==0:
            return True
        return False
    
    @staticmethod
    def record(self, currentGen):
        'empty'

    def _recordMessaging(self, currentGen):
        if self.printStatus == True:
            print(f'Recorded generation {currentGen.gen}')
        # print(currentGen.gen)
        
    def _setPrintStatus(self, printStatus):
        self.printStatus = printStatus



class basicRecorder(Recorder):
    """
    A recorder that stores basic inforamtion about each generation. 
    This includes the absolute best score, and a pool of best individuals.
    It's also possible to control which generations get saved.
    
    Caution should be taken with large analyses, it's possible to run out of 
    memory and crash the analysis.
    

    Parameters
    ----------
    recordEvery : int
        The number of generations between record points. i.e. if set equal to 3
        generations 3, 6, 9 etc. will be stored.
    Nstore : int, optional
        The number of individuals to store after each generation. Individuals
        are chosen based on their score, where those with a highest score are
        chosen first.
        The default is 1.
    printStatus : bool, optional
        A toggle that turns on or off printing messages. The default is True.

    Returns
    -------
    None.
    """



    def record(self, currentGen):
        
        if self.shouldRecord(currentGen.gen) == False:
            return
        # print(currentGen.gen)
        # Record the best of each generation
        self._recordMessaging(currentGen)
        self.data.genNumber.append(currentGen.gen)
        self.recordBestAbsolute(currentGen)
        self.recordBestPool(currentGen)
        
        
    def recordBestAbsolute(self, currentGen):
        """
        Records the single best geontype, individual and value
        """
        self.data.bestIndividuals.append(currentGen.best)
        self.data.bestGenotypes.append(currentGen.best.genotype)
        self.data.bestScores.append(currentGen.bestScore)

    def recordBestPool(self, currentGen):
        """
        Records the best Nstore individuals of the current generation in
        a population.
        """
        
        keepInexes  = np.argsort(currentGen.scores)[:self.Nstore]
        tempPop     = np.array(currentGen.population)
        
        storedIndividuals = tempPop[keepInexes]
        self.data.populations.append(storedIndividuals)
        self.data.populationBestScores.append(currentGen.scores[keepInexes])
        



class liteRecorder(Recorder):
    
    def __init__(self, recordEvery: int):
        super().__init__(recordEvery)
            
    def record(self, currentGen):
        
        if self.shouldRecord(currentGen.gen) == False:
            return
                    
        # Record the best of each generation
        self.data.genNumber.append(currentGen.gen)
        self.recordBestAbsolute(currentGen)
        
    def recordBestAbsolute(self, currentGen):
        """
        Records the single best geontype, individual and value
        """
        self.data.bestScores.append(currentGen.bestScore)       


# =============================================================================
# 
# =============================================================================

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
        
    
    
    
def pickleData(geneticAlgorithm, fileName):
    """
    Saves the current generation as a pickle.
    
    """
    
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
    
    """
    Reads a saved pickle.
    """
    

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