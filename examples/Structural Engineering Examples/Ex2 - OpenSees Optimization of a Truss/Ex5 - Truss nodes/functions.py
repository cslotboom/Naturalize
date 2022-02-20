# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: CS
"""

import naturalize as nat
import numpy as np
import random

import sys
sys.path.append('..')
import TrussAnalysis as ta


class environment:
    
    def __init__(self, gridSize, xlims, ylims, trussMat = 11, forces = np.array([1000., 1000., 0.])):
        self.gridSize = gridSize
        self.Npoint = gridSize**2
        
        self.xlims = xlims
        self.ylims = ylims
        
        self.dx = self.xlims[1] - self.xlims[0]  
        self.dy = self.ylims[1] - self.ylims[0]  
        
        self.trussMat = trussMat
        self.forces = forces
        
    def getCoords(self, nodeGenes):
        """
        Gets the input coordinants, assuming that 

        Parameters
        ----------
        nodeGenes : array
            DESCRIPTION.

        Returns
        -------
        xyCoords : TYPE
            DESCRIPTION.

        """
        xposition = nodeGenes % self.gridSize
        
        remainder = nodeGenes - xposition
        yposition = remainder / self.gridSize
        
        # We offset our grid so it is centered around the boundary
        # otherwise our grid would not extend to the end of our domain
        xCoords = (xposition / (self.gridSize - 1))* self.dx + self.xlims[0]
        yCoords = (yposition / (self.gridSize - 1))* self.dy + self.ylims[0]

        xyCoords = np.column_stack([xCoords, yCoords])
        return xyCoords     


    def getNodeGene(self):
        return random.randrange(self.Npoint)



 

def getNodes():
    
    baseX = np.array([0.,1.,1.])
    baseY = np.array([0.,0.,3.])
    
    basexy = np.column_stack([baseX, baseY])

    

class genePool(nat.BasicGenePool):
    
    # This ain't pretty but it gets the job done.
    # a more elengant solution would premit lbounds and ubounds to be different sized.
    def getGene(self, lbounds, ubounds):
        """ generates a random array of integers between the upper and lower
        bound, equal to the size of the gene"""
        return np.random.randint(lbounds[0], ubounds[0], len(lbounds))
    
    def getGenotype(self):
        """
        Gets all genes and stores it in a container
        """
        
        Ngenes = len(self.llims)
        genotype = []
        for ii in range(Ngenes):
        
            lbounds = self.llims[ii]
            ubounds = self.ulims[ii]
            # rand = np.random.randint(lbounds[0],)
            genotype.append(self.getGene(lbounds,ubounds))
        
        return genotype

            
def testIndividual(individual, env):
    """
    Tests and individual and returns the result of that test.
    
    The user should consider if it's possible for the test not to work.
    
    This is an interface that converts the inputs of the invididual to the 
    more generic inputs of the truss analysis
    
    """
    
    # Test outcomes:
    # The attempt at testing the individual did not work.
    
    # The test did work, and there is a score.
    
    # Passing all of these in is a little messy.
    Areas = np.ones(11)*0.001
    Forces = env.forces
    # xyNodes = env.getCoords(individual.genotype[0])
    # xCoords = xyNodes[:,0]
    # yCoords = xyNodes[:,1]
    
    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]
    xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])

      
    xCoordBasic = np.array([0.,1.,1.])
    yCoordBasic = np.array([0.,0.,3.])
    
    
    # Add the basic node and the final fixed node.
    xCoords = np.concatenate([xCoordBasic[:2], xCoords, [xCoordBasic[-1]]])
    yCoords = np.concatenate([yCoordBasic[:2], yCoords, [yCoordBasic[-1]]])
    
    Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    
    
    gen = str(individual.gen)
    nodeIDs = np.array([1,2,3,4,5,6,7])
    
    disp, volumes, force = ta.runTrussAnalysis(Areas, Forces, nodeIDs, xCoords, yCoords, Connectivity, env.trussMat)
    # ta.plotTruss(Areas, xCoords, yCoords, Connectivity)
    # print('Truss') # debugging
    # return disp, volumes, force
    return disp, volumes

def plotIndividual(individual, env):
    
    
    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]
    
    
    xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])

      
    xCoordBasic = np.array([0.,1.,1.])
    yCoordBasic = np.array([0.,0.,3.])
    
    xCoords = np.concatenate([xCoordBasic[:2], xCoords, [xCoordBasic[-1]]])
    yCoords = np.concatenate([yCoordBasic[:2], yCoords, [yCoordBasic[-1]]])
    nodeIDs = np.array([1,2,3,4,5,6,7])
    Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]       
    Areas = np.ones(11)*0.001
    ta.plotTruss(Areas,nodeIDs, xCoords, yCoords, Connectivity)


def ftest(individual, environment):
    
    """
    Note that our OpenSees analysis may actually fail to converge for some 
    geneotypes. Here we use a try/except block to try and catch these errors.
    
    It's not perfect, sometimes Opensees still manages to crash the kernal.. 
    This is beyound our control, but doesn't happen very often.
    
    """
    
    try:
        result = testIndividual(individual, environment)
        # print('result')  # debugging
    except:
        result = [10**6, [10**6]]
        print(str(individual.name) + ' failed')
        
    # if result[0] == 0:
    #     result[0] = 10**6
    individual.result = result
    return result




def fitness(individual, environment):
    
    """
    Determines how good each solution is.
    Here we used a normalized displacement, which is the displacement multiplied
    by the total volume.
    
    THe best solution will have the lowest combination of displacement and volume.
    """
    
    # Npoint = len(route)
    # Indexes = np.arange(Npoint)
    
    # disp, volumes, forces = individual.result
    disp, volumes = individual.result
    
    # normDisp = np.sum(disp)
    
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 100
    else:
        fitness = disp[0]    
    # print('fit') # debugging
    return fitness


def fitnessComplex(individual, environment):
    
    """
    Determines how good each solution is.
    Here we used a normalized displacement, which is the displacement multiplied
    by the total volume.
    
    THe best solution will have the lowest combination of displacement and volume.
    """
    
    dispLim = 3/250
    # forceLim = 16000
    
    disp, volumes = individual.result
    
    vol = np.sum(volumes)
    # forces = np.abs(forces)
    # maxForce = np.max(forces)
    
    fitness = disp[0]*vol
    
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 100
    
    # if 
    
    # We
    # if dispLim < disp[0]:
    #     fitness = 100
        # RR
    # if forceLim < maxForce:
    #     fitness = 100   
    
    return fitness


def fitnessLength(individual, environment):
    
    """
    Determines how good each solution is.
    Here we used a normalized displacement, which is the displacement multiplied
    by the total volume.
    
    THe best solution will have the lowest combination of displacement and volume.
    """
    
    Llim = 1.5
    
    disp, volumes = individual.result
    
    
    Lmax = np.max(np.array(volumes) / 0.001)
    Lmin = np.min(np.array(volumes) / 0.001)
    
    fitness = disp[0]
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 100
        # normDisp = 100
    if Llim < Lmax:
        fitness = 100
    # if Lmin < 0.3:
    #     fitness = 100
    
        # We
    # if dispLim < disp:
    #     fitness = 100
    
    return fitness
