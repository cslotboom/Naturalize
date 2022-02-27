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
mm = 0.001

class environment:
    """
    The enviroment will act as a container for the data in the problem.
    The boundary node coordinates and element fixities are defined as static 
    values.
    """

    def __init__(self, xlims, ylims, trussMat = 11, forces = np.array([1000., 1000., 0.])):
        
        """
        Set the limits and define their size.
        """
        
        self.xlims = xlims
        self.ylims = ylims
        self.dx = self.xlims[1] - self.xlims[0]  
        self.dy = self.ylims[1] - self.ylims[0]  
        """
        Set the truss material and forces and define their size.
        """

        self.trussMat = trussMat
        self.forces = forces
        
        """
        Set the static boundary nodes, and the connectivities between nodes.
        """
        
        self.xCoordBasic = np.array([0.,1.,1.])
        self.yCoordBasic = np.array([0.,0.,3.])
        self.Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    

            
def testIndividual(individual, env):
    """
    Tests and individual and returns the result of that test.
    This function essentially is a wrapper that converts data from our 
    individual and environment into a form usable by the truss anaylsis
    functions.

    Note several values are returned as a result. 
    This will be processed later to define the value of fitness.      
    
    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    """

    Areas = np.ones(11)*100*mm**2
    Forces = env.forces
    
    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]
    xCoordBasic  = env.xCoordBasic
    yCoordBasic  = env.yCoordBasic
    connectiviy = env.Connectivity
    
    # Add the basic node and the final fixed node.
    xCoords = np.concatenate([xCoordBasic[:2], xCoords, [xCoordBasic[-1]]])
    yCoords = np.concatenate([yCoordBasic[:2], yCoords, [yCoordBasic[-1]]])
    
    gen = str(individual.gen)
    nodeIDs = np.array([1,2,3,4,5,6,7])
    
    disp, volumes, force = ta.runTrussAnalysis(Areas, Forces, nodeIDs, xCoords, yCoords, connectiviy, env.trussMat)
    return disp, volumes, force


def ftest(individual, environment):
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


def fitness_basic(individual, environment):
    """
    Determines how good each solution is, this is what that is minimized 
    In this case, minimize the displacement in the x direction.

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

    
    # disp, volumes, forces = individual.result
    disp, volumes, _ = individual.result
    
    
    """
    Sometimes OpenSees freaks out and returns a negative displacement.
    We don't want those solutions!"""
    if disp[0] <= 0:
        fitness = 100
    else:
        fitness = disp[0]    
    return fitness


def fitness_Complex(individual, environment):
    
    """
    Determines how good each solution is, this is what that is minimized. 
    In this function, the displacement multiplied by volume is minimized.

    This will make solutions with a lower volume more attractive.

    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    Returns
    -------
    fitness : float
        The output displacement multiplied by system volume.

    """
    
    dispLim = 3/250
    # forceLim = 16000
    
    disp, volumes, _ = individual.result
    
    vol = np.sum(volumes)
    
    fitness = disp[0]*vol
    
    # Sometimes opensees freaks out and returns a negative displacement.
    # We don't want those solutions!
    if disp[0] <= 0:
        fitness = 100
    
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

    if disp[0] <= 0:
        fitness = 100
        # normDisp = 100
    if Llim < Lmax:
        fitness = 100

    return fitness







def plotIndividual(individual, env):
      
    xCoordBasic  = env.xCoordBasic
    yCoordBasic  = env.yCoordBasic
    connectiviy = env.Connectivity

    xCoords = individual.genotype[0]
    yCoords = individual.genotype[1]
    
    xCoords = np.concatenate([xCoordBasic[:2], xCoords, [xCoordBasic[-1]]])
    yCoords = np.concatenate([yCoordBasic[:2], yCoords, [yCoordBasic[-1]]])
    nodeIDs = np.array([1,2,3,4,5,6,7])
    Areas = np.ones(11)*0.001
    fig, ax = ta.plotTruss(Areas,nodeIDs, xCoords, yCoords, connectiviy)
    
    areas = np.ones(len(connectiviy))
    maxArea = 1
    style_blue(fig, ax, areas, maxArea)
    return fig, ax






def style_blue(fig, ax, areas, maxArea):
    
    fig.set_figwidth(8)
    fig.set_figheight(6)

    for text in ax.texts:
        text.set_fontsize(10)
    ax.texts = []






    for ii, line in enumerate(ax.lines):
        line.set_linewidth(5*areas[ii]/maxArea)
        line.set_color("steelblue")
    ax.set_facecolor("skyblue")
    ax.collections[0].set_color('cornsilk')
    ax.collections[0].set_zorder(10)
    ax.collections[0].set_linewidth(2)
    # fig.savefig("mygraph.png")
    # ax.axis('off')
    ax.set_xlim([-1.5, 2.5])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # ax.annotate("", xy=(0.9, 3), xytext=(0.5, 3),  arrowprops=dict(arrowstyle="->", color = 'red') )
    return fig, ax










