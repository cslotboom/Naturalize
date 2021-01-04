# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""


import numpy as np
import matplotlib.pyplot as plt


def getGenes(Analysis, geneIndex):
    Ngen = Analysis.Ngen
    Npop = Analysis.Npopulation
    geneVals = np.zeros([Ngen, Npop])
    
    for ii in range(Ngen):
        # Get the genome
        tempGenome = np.array(Analysis.gens[ii].getCurrentGenome())
        geneVals[ii,:] = tempGenome[:,geneIndex]
        
    return geneVals        


# def getGenomes(Analysis, geneIndex):
#     Ngen = Analysis.Ngen
#     Npop = Analysis.Npopulation
#     genomes = np.zeros([Ngen, Npop])
    
#     for ii in range(Ngen):
#         # Get the genome
#         tempGenome = np.array(Analysis.gens[ii].getCurrentGenome())
        
#     return geneVals     


def initFig(Analysis):
    fig, ax = plt.subplots()
    
    return fig, ax






def plotAvgGene(fig, ax, Analysis, geneIndex):
    Genes = getGenes(Analysis, geneIndex)
    avgGenes = np.average(Genes, 1)     
                
    ax.plot(avgGenes)

def plotMinGene(fig, ax, Analysis, geneIndex):
    Genes = getGenes(Analysis, geneIndex)
    ymin = np.min(Genes, 1)     
                
    ax.plot(ymin)


def plotAvgFitness(fig, ax, Analysis):
    Ngen = Analysis.Ngen
    scoreAvg = np.zeros(Ngen)
    
    for ii in range(Ngen):       
        scoreAvg[ii] = np.average(Analysis.gens[ii].scores)
            
    ax.plot(scoreAvg)

def plotMinFitness(fig, ax, Analysis):

    Ngen = Analysis.Ngen
    scoreBest = np.zeros(Analysis.Ngen)
    
    for ii in range(Ngen):              
        scoreBest[ii] = np.min(Analysis.gens[ii].scores)
    
    ax.plot(scoreBest)



def plotTotalFitness(fig, ax, Analysis):
    BestOverTime = np.zeros(Analysis.Ngen)
    BestOverTime = Analysis.BestValues
    
    ax.plot(BestOverTime)

# yAvg = np.zeros(Ngen)
# ybest = np.zeros(Ngen)
# scoreAvg = np.zeros(Ngen)
# scoreBest = np.zeros(Ngen)

# BestOverTime = np.zeros(Ngen)

# for ii in range(Ngen):
#     # Get the genome
#     out = np.array(algorithm.gens[ii].getCurrentGenome())
#     yAvg[ii] = -np.average(out[:,1])
#     ybest[ii] = -np.min(out[:,1])
    
#     scoreAvg[ii] = -np.average(algorithm.gens[ii].scores)
    
#     scoreBest[ii] = -np.min(algorithm.gens[ii].scores)
#     scoreBest[ii] = -np.min(algorithm.gens[ii].scores)
    
# BestOverTime = algorithm.BestValues
# print(algorithm.gens[5].getCurrentGenome())

# fig, ax = plt.subplots()
# plt.plot(yAvg)
# plt.plot(ybest)

# fig, ax = plt.subplots()
# plt.plot(scoreAvg)
# plt.plot(scoreBest)

        
    
            