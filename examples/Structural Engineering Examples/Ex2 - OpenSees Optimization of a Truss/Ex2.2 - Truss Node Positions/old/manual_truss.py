# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


from functions import ftest, fitness, environment, genePool, plotIndividual
from TrussAnalysis import runTrussAnalysis, plotTruss
import numpy as np

Areas = np.ones(11)*0.001
Forces = np.array([1000., 1000., 0.])

Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]    

xCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
yCoords = np.array([0.,0.,1.,1.,2.,2.,3.])



trussMat = 10


disp, vol, force = runTrussAnalysis(Areas, Forces, xCoords, yCoords, Connectivity, trussMat)


xy = np.array([[0.5 , 1.92],
           [1.82, 1.57],
           [0.53, 1.95],
           [1.96, 1.98]])


xCoords = [0., 1, *xy[:,0], 1]
yCoords = [0., 0, *xy[:,1], 3]

disp, vol, force = runTrussAnalysis(Areas, Forces,xCoords, yCoords, Connectivity, trussMat)

plotTruss(Areas, xCoords, yCoords, Connectivity)