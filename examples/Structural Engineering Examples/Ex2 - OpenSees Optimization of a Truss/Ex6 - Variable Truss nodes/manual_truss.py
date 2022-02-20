# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""

import numpy as np
import openseespy.opensees as op
import sys
sys.path.append('..')
from functions import ftest, fitness, environment, genePool, plotIndividual
from TrussAnalysis import runTrussAnalysis, plotTruss


Areas = np.ones(11)*0.001
Forces = np.array([1000., 1000., 0.])
Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    

xCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
yCoords = np.array([0.,0.,1.,1.,2.,2.,3.])

trussMat = 10
nodeIds = np.arange(len(Connectivity)) + 1


disp, vol, force = runTrussAnalysis(Areas, Forces, nodeIds, xCoords, yCoords, Connectivity, trussMat)


xy = np.array([[0.5 , 1.92],
               [1.82, 1.57],
               [0.53, 1.95],
               [1.96, 1.98]])


xCoords = [0., 1, *xy[:,0], 1]
yCoords = [0., 0, *xy[:,1], 3]

disp, vol, force = runTrussAnalysis(Areas, Forces,nodeIds,xCoords, yCoords, Connectivity, trussMat)
print(op.nodeDOFs(4))

plotTruss(Areas,nodeIds, xCoords, yCoords, Connectivity)




# =============================================================================
# Basic truss testing
# =============================================================================

# xCoords = [0., 1,  1]
# yCoords = [0., 0, 3]
# Connectivity = [[1,2],[1,3],[2,3]]
# plotTruss(Areas, xCoords, yCoords, Connectivity)

# disp, vol, force = runTrussAnalysis(Areas, Forces,xCoords, yCoords, Connectivity, trussMat,3)

# op.reactions()
# op.nodeDisp(3)
# op.nodeReaction(2)

# =============================================================================
# 
# =============================================================================




Areas = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001,
        0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001,
        0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001,
        0.001])

Forces = np.array([0., 0.,    0.])    

nodeX = np.array([1.  , 2.  , 1.99, 1.6 , 0.6 , 1.9 , 1.24, 1.58, 1.99])
nodeY = np.array([0.  , 0.  , 2.  , 0.2 , 0.73, 0.07, 1.94, 0.39, 2.  ])

Connectivity = np.array([[1, 2],
                    [1, 3],
                    [1, 4],
                    [1, 5],
                    [1, 6],
                    [1, 7],
                    [1, 8],
                    [2, 3],
                    [2, 4],
                    [2, 5],
                    [2, 6],
                    [2, 7],
                    [2, 8],
                    [3, 4],
                    [3, 5],
                    [3, 6],
                    [3, 7],
                    [3, 8],
                    [4, 5],
                    [4, 6],
                    [4, 7],
                    [4, 8],
                    [5, 6],
                    [5, 7],
                    [5, 8],
                    [6, 7],
                    [6, 8],
                    [7, 8]])

# trussMat = 10
# loadNode = 3
plotTruss(Areas,nodeIds, nodeX, nodeY, Connectivity)

disp, vol, force = runTrussAnalysis(Areas, Forces, nodeIds, nodeX, nodeY, Connectivity, trussMat)
