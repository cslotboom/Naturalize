# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""

import openseespy.opensees as op
import openseespy.postprocessing.Get_Rendering as opp


import numpy as np
import os 

kN = 1000
# def buildTruss(Areas, xNodeCoords, yNodeCoords, Connectivity):
    
#     trussMat = 10
#     Volume = [None]*len(Areas)
    
#     # xNodeCoords = np.array([0.,1.,0.,1.,0.,1.,1.])
#     # yNodeCoords = np.array([0.,0.,1.,1.,2.,2.,3.])
#     Nnodes = len(xNodeCoords)
    
#     # Connectivity = [[1,2],[1,4],[2,4],[1,3], [3,4],[3,6],[3,5],[4,6], [5,6], [5,7], [6,7]]
    
    
#     for ii in range(Nnodes):
#         ID = int(ii + 1)
#         op.node(ID,  xNodeCoords[ii], yNodeCoords[ii],  '-ndf', 3)
#         # op.node(2,  0., 0.,  '-ndf', 3)
#         if ii ==1 or ii == 2:
#             op.fix(ID,1,1,1)
#         else:
#             op.fix(ID,0,0,1)
                
#     tempL = 0.
#     for ii, connect in enumerate(Connectivity):
#         ID = int(ii + 1)
#         op.element("truss " , ID  , *connect, Areas[ii], trussMat)
        
#         p1 = np.array(op.nodeCoord(connect[0]))
#         p2 = np.array(op.nodeCoord(connect[1]))
        
#         tempL = (np.sum((p1 - p2)**2))**0.5
        
#         Volume[ii] = Areas[ii]*tempL


#     return Volume


# def getSections():
    
#     Fu = 5*kN
#     k = 4*10**9
#     b = 0.001
#     op.uniaxialMaterial( 'Steel02', 10,  Fu,  k, b, 18., .925, 0.15)
    
#     ERelease = 1.
#     op.uniaxialMaterial( 'Elastic' ,  2,  ERelease,  0.0 )
    
#     ## Define geometric transformation(s) 
#     ## ---------------------------------- 
#     #geomTransf('Linear',1) 
#     op.geomTransf('PDelta',1)
#     op.beamIntegration('Lobatto',1,1,3)


# def applyLoads(Forces):
#     op.timeSeries('Linear',1,'-factor' ,1.0)  
#     op.pattern  ('Plain',1, 1,  '-fact', 1.) 
#     op.load(7, *Forces/10)


# def defineBasicAnalysis():
                            
#     # op.initialize() 
#     op.constraints("Plain")
#     op.numberer("Plain")
#     # System of Equations 
#     op.system("UmfPack", '-lvalueFact', 10)
#     # Convergence Test 
#     op.test('NormDispIncr',  1.*10**-8, 25, 0 , 2)
#     # Solution Algorithm 
#     op.algorithm('Newton')
#     # Integrator 
#     op.integrator('LoadControl', 1, 1)
#     # Analysis Type 
#     op.analysis('Static')

    
def runTrussAnalysis(Areas, Forces, xNodeCoords, yNodeCoords, Connectivity):
    """
    Tests and individual and returns the result of that test.
    
    The user should consider if it's possible for the test not to work.
    
    """
    
       
    op.wipe()
    op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )

    # Step size
    dx = 0.0001
    ControlNode = 7
    controlDof = 1

    # Define geometry 
    # ---------------
    getSections()
    
    volume = buildTruss(Areas, xNodeCoords, yNodeCoords, Connectivity)
    
    applyLoads(Forces)
    
    # Define Analysis Parameters
    # ----------------- 
    defineBasicAnalysis()

    # opp.plot_model()
    
    op.record()
    
    for ii in range(10):
        op.analyze(1)
                    
    disp = op.nodeDisp(ControlNode, controlDof)
    
    return disp, volume




# def runTrussAnalysis():
    
#     pass






