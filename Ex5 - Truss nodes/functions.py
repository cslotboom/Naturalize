# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as test
import numpy as np
import sys
import TrussAnalysis as ta





def getNewNode(rand, llims, ulims):
    """
    Rand is a 2D array of two random floats
    """
    
    Nodexy = rand*(ulims - llims) + llims

    
    return Nodexy





def testIndividual(individual):
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
    Areas = individual.genome
    Forces = np.array([1000., 1000., 0.])
    xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])    
    Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    
    
    gen = str(individual.gen)
    name = str(individual.name)
    print(name)    
    
    
    disp, volumes = ta.runTrussAnalysis(Areas, Forces, xNodeCoords, yNodeCoords, Connectivity)

    return disp, volumes



def ftest(individual, environment):
    result = testIndividual(individual)
    individual.result = result
    return result




def fitness(individual, environment):
    # Npoint = len(route)
    # Indexes = np.arange(Npoint)
    
    disp, volumes = individual.result
    
    # Normalized Disp
    normDisp = disp * np.sum(volumes)
    
    return normDisp
