# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: CS

Check the read-me file for a summary of the problem
"""

import numpy as np
import sys
sys.path.append('..')
import TrussAnalysis as ta


class environment:
    """
    The enviroment will act as a container for the data in the problem.
    The node coordinates and element fixities are defined as fixed values.
    """
    
    def __init__(self, forces = np.array([1000., 1000., 0.]),trussMat = 10):
        self.forces = forces
        self.xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
        self.yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])
        self.Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]] 
        self.nodeIds = np.arange(len(self.Connectivity)) + 1
                
        self.trussMat = trussMat
      
def ftest(individual, environment):
    """
    Tests and individual and returns the result of that test.
    This function essentially is a wrapper that converts data from our 
    individual and environment into a form usable by the truss anaylsis
    functions.

    Note several values are returned as a result. 
    We'll later process these to define our fitness value.      
    
    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    """

    
    
    Areas = individual.genotype[0]
    
    """
    Make the truss defined in the problem definition. This is fixed.
    We could condense this by returning a list and passing that list in with a 
    *List to the function, however, we'll write it out explicitly for this 
    example to be clear'
    """
    Forces = environment.forces
    xNodeCoords = environment.xNodeCoords
    yNodeCoords = environment.yNodeCoords 
    Connectivity = environment.Connectivity
    trussMat = environment.trussMat
      
    nodeIds = environment.nodeIds
    result = ta.runTrussAnalysis(Areas, Forces, nodeIds, xNodeCoords, 
                                 yNodeCoords, Connectivity, trussMat)    
    disp, volume, Forces     = result
    return disp, volume, Forces 




def fitness_basic(individual, environment):
    """
    The fitness function, this is what we actually want to minimize.
    In this case, we'll minimize the displacement in the x direction.

    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    Returns
    -------
    disp : float
        The output displacement of the analysis.

    """
        
    disp, volumes, _ = individual.result
    
    dx = disp[0]
    disp = np.abs(dx)
    return disp



def fitness_normalized(individual, environment):
    """
    The fitness function, this is what we actually want to minimize.
    In this case, we'll minimize the displacement multiplied by the volume.
    This will make solutions with a lower volume more attractive.

    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    Returns
    -------
    normDisp : float
        The output displacement of the analysis.

    """
    disp, volumes, _ = individual.result
    dx = disp[0]
    normDisp = np.abs(dx * np.sum(volumes))
    
    return normDisp





def plotIndividual(data):
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
    Areas = data
    Forces = np.array([1000., 1000., 0.])
    xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])    
    Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    
    
    
    # gen = str(individual.gen)
    # name = str(individual.name)
    # print(name)    
    nodeIds = np.arange(len(Connectivity)) + 1
    
    return ta.plotTruss(Areas, nodeIds, xNodeCoords, yNodeCoords, Connectivity)











