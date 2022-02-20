# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as nat
import numpy as np
# import sys
import random

import sys
sys.path.append(r'C:\Users\Christian\Scripts\CodingAdventures\GeneticAlgorithms\Package')
import TrussAnalysis as ta



class environment:
    
    def __init__(self, gridSize, trussMat = 11, forces = np.array([1000., 1000., 0.]),
                 Nnodes = 20, Nstatic = 3):
        self.gridSize = gridSize
        self.Npoint = gridSize**2
                
        self.trussMat =trussMat
        self.forces = forces
        
        self.Nnodes = Nnodes
        self.Nconnect = int(Nnodes*(Nnodes-1)/2)
        
        # sets teh 
        self.setConnectionsList()
        self.setConnectivityMatrix()
        
        self.Nstatic = Nstatic
 
      
    def setConnectionsList(self):
        """
        Makes a list of all possible connections
        """
        pairs = []
        Nnodes = self.Nnodes
        for ii in range(Nnodes):
            start = ii + 1
            
            jj = 1
            while jj + start <= Nnodes:
                end = start + jj
                pairs.append([start, end])
                jj +=1
        
        self.connections = np.array(pairs)
        
    def setConnectivityMatrix(self):
        """
        Makes a matrix of all possible connections?
        """
        Nnodes = self.Nnodes
        Nconnect = self.Nconnect
        mapArray = np.ones([Nconnect, Nnodes])
        
        
        m1 = 0
        dN = Nnodes - 1
        m2 = dN - 1
        
        Indexes = [None]*Nnodes
        baseIndex = np.linspace(m1, m2, dN, dtype = int)
        Indexes[0] = baseIndex
        
        m1 = m1 + dN       

        Ind = np.array(baseIndex)
        mapArray[Ind,0] = 0
        breaks = np.zeros(Nnodes)
        for ii in range(1, Nnodes):
            
            breaks[ii] = m1
            dN = Nnodes - 1 - ii
            m2 = m1 + dN - 1
            
            baseGroup = np.linspace(m1, m2, dN, dtype = int)
            
            m1 = m1 + dN
                
            existing = []
            for jj in range(ii):
                existing.append(int(breaks[jj] + ii - jj - 1))
            Ind = np.concatenate([baseGroup,existing])
            
            
            mapArray[Ind,ii] = 0
            
        self.connectMatrix = mapArray
    
    
    def getConncetivityMask(self, nodeMaskGene):
        Nnodes = self.Nnodes
        Nconnect = self.Nconnect
        connectMatrix = self.connectMatrix
        
        tempMapArray = np.zeros([Nconnect,Nnodes], dtype = bool)
        for ii, val in enumerate(nodeMaskGene):
            if val == 1:
                tempMapArray[:,ii] = 1
                # tempMapArray[:,ii] = connectMatrix[:,ii]
            else:
                tempMapArray[:,ii] = connectMatrix[:,ii]
                # tempMapArray[:,ii] = 1
            
        connections = np.product(tempMapArray,1,dtype=bool)
        # connections = ~remove
        return connections
        
    # def getPairs
    
    def getConncetivity(self, nodeMask, connectGene):
        
        connectMask = self.getConncetivityMask(nodeMask)
        connFiltered = connectMask*connectGene
        
        return self.connections[connFiltered]
        
    
    # def getConnectivityGene(self):
    #     return random.randrange(self.Npoint)
    
    
    # def setConnectivityKeys(self):
    #     connections = []
    #     Nnode = 4
    #     for ii in range(Nnode):
    #         start = ii + 1
            
    #         jj = 1
    #         while jj + start <= Nnode:
    #             end = start + jj
    #             connections.append([start, end])
    #             jj +=1
                
    #     self.connections = np.array(connections)
    
    def getConnections(self):
        return random.randrange(self.Npoint)


def getNewNode(rand, llims, ulims):
    """
    Rand is a 2D array of two random floats
    """
    
    Nodexy = rand*(ulims - llims) + llims

    
    return Nodexy


# def getNodes():
    
#     baseX = np.array([0.,1.,1.])
#     baseY = np.array([0.,0.,3.])
    
#     basexy = np.column_stack([baseX, baseY])



# def getConnectivity()
    

class genePool(nat.BasicGenePool):

    """
    gene1: x vector
    gene1: y vector
    gene2: Connectivity vector
    gene3: Node Mask
    
    """    

    def setStaticNodes(self, staticx, staticy):
        """
        The static nodes are always the first several nodes in the 

        """
        self.staticx = staticx
        self.staticy = staticy
        self.Nstatic = len(staticx)
        
    def getNewIntGene(self, lbounds, ubounds):
        """ generates a random array of integers between the upper and lower
        bound, equal to the size of the gene"""
        return np.random.randint(lbounds[0], ubounds[0], len(lbounds))
    
    def getNewGenotype(self):
        """
        Gets all genes and stores it in a container
        """
        
        Ngenes = len(self.llims)
        genotype = []
        for ii in range(Ngenes):
        
            lbounds = self.llims[ii]
            ubounds = self.ulims[ii]
            # rand = np.random.randint(lbounds[0],)
            if ii > 1: # genes 2/3 are ints
                genotype.append(self.getNewIntGene(lbounds,ubounds))
            else: # genes 0/1 are flaots
                rand = np.random.random(len(lbounds))
                genotype.append(self.getNewGene(rand,lbounds,ubounds))
        
        
        # make the first and final nodes load nodes
        genotype[3][0:2] = True
        genotype[3][-1] = True
        
        # Convert the connectivity gene and node mask to boolean
        genotype[0][:self.Nstatic] = self.staticx 
        genotype[1][:self.Nstatic] = self.staticy 
        genotype[2] = np.array(genotype[2], dtype = bool)
        genotype[3] = np.array(genotype[3], dtype = bool)
        
        
        return genotype

            
def testIndividual(individual, env):
    """
    Tests and individual and returns the result of that test.
    
    The user should consider if it's possible for the test not to work.
    
    This is an interface that converts the inputs of the invididual to the 
    more generic inputs of the truss analysis
    
    """
    
        
    """
    gene1: position vector
    gene2: Connectivity vector
    gene3: Node Mask
    
    """      

    Forces = env.forces   
    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]

    connectGene = np.array(individual.genotype[2], bool)
    nodeMask = np.array(individual.genotype[3], bool)    
    
    
    Nnodes = len(xCoords)
    nodeIDs = np.arange(1,Nnodes +0.1)
    Nstatic = env.Nstatic - 1
    
    # staticNode = env.staticNode
    
    # Rearrange the coordinats - our model fixes the last one 
    xCoords = np.concatenate([xCoords[:Nstatic], xCoords[Nstatic+1:], [xCoords[Nstatic]]])
    yCoords = np.concatenate([yCoords[:Nstatic], yCoords[Nstatic+1:], [yCoords[Nstatic]]])
    
    xCoords = xCoords[nodeMask]
    yCoords = yCoords[nodeMask]
    nodeIDs = nodeIDs[nodeMask]

    Connectivity = env.getConncetivity(nodeMask, connectGene) 
    Nele = len(Connectivity)
    Areas = np.ones(Nele)*0.001
    
    # Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    
    
    # gen = str(individual.gen)
    
    
    disp, volumes, force = ta.runTrussAnalysis(Areas, Forces, nodeIDs, xCoords, yCoords, Connectivity, env.trussMat, 8)
    # ta.plotTruss(Areas, xCoords, yCoords, Connectivity)
    # print('Truss') # debugging
    # return disp, volumes, force
    return disp, volumes

def plotIndividual(individual, env):
    
    # Areas = np.ones(11)*0.001

    # xyNodes = env.getCoords(individual.genotype[0])
    # xCoords = xyNodes[:,0]
    # yCoords = xyNodes[:,1]
    # xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    # yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])

      
    # xCoordBasic = np.array([0.,1.,1.])
    # yCoordBasic = np.array([0.,0.,3.])
    
    # xCoords = np.concatenate([xCoordBasic[:2], xCoords, [xCoordBasic[-1]]])
    # yCoords = np.concatenate([yCoordBasic[:2], yCoords, [yCoordBasic[-1]]])
    
    # Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    
    
    # Forces = env.forces   
    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]    
    # nodeCordGene = individual.genotype[0]
    connectGene = np.array(individual.genotype[2], bool)
    nodeMask = np.array(individual.genotype[3], bool)
    
    # xyNodes = env.getCoords(nodeCordGene)
    # xCoords = xyNodes[:,0]
    # yCoords = xyNodes[:,1]
    
    Nnodes = len(xCoords)
    nodeIDs = np.arange(1,Nnodes +0.1)
    Nstatic = env.Nstatic - 1
    
    # Rearrange the coordinats - our model fixes the last one 
    xCoords = np.concatenate([xCoords[:Nstatic], xCoords[Nstatic+1:], [xCoords[Nstatic]]])
    yCoords = np.concatenate([yCoords[:Nstatic], yCoords[Nstatic+1:], [yCoords[Nstatic]]])
    
    xCoords = xCoords[nodeMask]
    yCoords = yCoords[nodeMask]
    nodeIDs = nodeIDs[nodeMask]
    
    Connectivity = env.getConncetivity(nodeMask, connectGene)
    Nele = len(Connectivity)
    Areas = np.ones(Nele)*0.001
    
    
    return ta.plotTruss(Areas, nodeIDs, xCoords, yCoords, Connectivity)


def ftest(individual, environment):
    
    """
    Note that our OpenSees analysis may actually fail to converge for some 
    geneotypes. Here we use a try/except block to try and catch these errors.
    
    It's not perfect, sometimes Opensees manages to crash the kernal.. 
    This seems to be random but doesn't happen very often.
    
    """
    
    try:
        result = testIndividual(individual, environment)
        # print('result')  # debugging
    except:
        result = [np.ones(3)*1000, [10**6]]
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
    
    Llim = 0.5
    
    disp, volumes = individual.result
    
    # If nothing i there, bad solution
    # if np.sum(volumes) == 0:
    #     return 100
    if len(volumes) != 0:
        Lmax = np.max(np.array(volumes) / 0.001)
        Lmin = np.min(np.array(volumes) / 0.001)
    else:
        Lmax = 1000
        Lmin = 1000
    
    fitness = disp[0]*Lmax
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 1000
        # normDisp = 100
    if Lmin < Llim:
        fitness = 1000
    # if np.sum(volumes) == 0:
    #     fitness = 100
    # if Lmin < 0.3:
    #     fitness = 100
    
        # We
    # if dispLim < disp:
    #     fitness = 100
    
    return fitness

def fitnessLength2(individual, environment):
    
    """
    Determines how good each solution is.
    Here we used a normalized displacement, which is the displacement multiplied
    by the total volume.
    
    THe best solution will have the lowest combination of displacement and volume.
    """
    
    Llim = 0.5
    
    disp, volumes = individual.result
    
    # If nothing i there, bad solution
    # if np.sum(volumes) == 0:
    #     return 100
    if len(volumes) != 0:
        Lmax = np.max(np.array(volumes) / 0.001)
        Lmin = np.min(np.array(volumes) / 0.001)
    else:
        Lmax = 0
        Lmin = 0
    
    fitness = disp[0]
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 1000
        # normDisp = 100
    if Lmin < Llim:
        fitness = 1000
    # if np.sum(volumes) == 0:
    #     fitness = 100
    # if Lmin < 0.3:
    #     fitness = 100
    
        # We
    # if dispLim < disp:
    #     fitness = 100
    
    return fitness
