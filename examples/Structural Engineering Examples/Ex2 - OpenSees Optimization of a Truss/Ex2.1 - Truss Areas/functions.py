# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: CS

Check the read-me file for a in-depth summary of the problem
"""

import numpy as np
import sys
sys.path.append('..')
import TrussAnalysis as ta


class environment:
    """
    The enviroment will act as a container for the data in the problem.
    The boundary node coordinates and element fixities are defined as static 
    values.
    """
    
    def __init__(self, forces = np.array([1000., 1000., 0.]),trussMat = 10):
        self.forces = forces
        
        """
        Here the nodes and connectivityies between each node are defined for 
        the problem. The connectivity assumes a 
        """
        
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
    This will be processed later to define the value of fitness.      
    
    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

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
        
    disp, volumes, _ = individual.result
    
    dx = disp[0]
    disp = np.abs(dx)
    return disp


def fitness_normalized(individual, environment):
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
    normDisp : float
        The output displacement of the analysis.

    """
    disp, volumes, _ = individual.result
    dx = disp[0]
    normDisp = np.abs(dx * np.sum(volumes))
    
    return normDisp


def fitness_Volume(individual, environment):
    """
    The fitness function, this value is what is actually minimized.
    In this case, the volume is minimized, assuming displacement is below some 
    limit. This will make solutions with a lower volume more attractive.

    Parameters
    ----------
    individual : Naturalize Indivdual
        The input indivdual.
    environment : Naturalize Environment
        The input environment.

    Returns
    -------
    volume : float
        The output volume of the truss.

    """
    
    
    disp, volumes, _ = individual.result
    dx = disp[0]
    
    """
    The limit could be placed within the environment function.
    """
    lim = 0.01
    if dx < lim:
        volume = np.sum(volumes)
    # normDisp = np.abs(dx * np.sum(volumes))
    else:
        volume = 100*np.sum(volumes)
    return volume


def plotIndividual(data):
    """
    Makes a matplotlib plot of the truss.
    """
    
    areas = data
    xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
    yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])    
    Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4], [3,6], [3,5], [4,6], [5,6], [5,7], [6,7]]    
    nodeIds = np.arange(len(Connectivity)) + 1
    fig, ax = ta.plotTruss(areas, nodeIds, xNodeCoords, yNodeCoords, Connectivity)
        
    maxArea = max(areas)
    style_blue(fig, ax, areas, maxArea)
    
    
    return fig, ax

def style_blue(fig, ax, areas, maxArea):
    
    """
    Used to make the animated plots
    """    
    
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



