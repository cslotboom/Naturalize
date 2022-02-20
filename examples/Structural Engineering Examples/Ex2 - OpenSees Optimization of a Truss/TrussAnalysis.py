# -*- coding: utf-8 -*-
"""
@author: CS

The following file defines functinos 

Funcitons are defined in the order that they will be called.
First the materials in the model are created, then 

"""

import openseespy.opensees as op
import openseespyvis.Get_Rendering as opp
import copy

import numpy as np
import os 

kN = 1000
GPa = 10*10**9

def getSections(Fu = 5.*kN, k = 200.*GPa, b = 0.001):
    """
    Creates the OpenSees sections and materials. Values are chosen arbitarly
    for stiffness. The yield stress and post yeild stiffness can be used to
    enforce an effective maximum force. After the yield stress, the member
    will deform significantly!

    Parameters
    ----------
    Fu : float, optional
        Yield force for the nonlinar material. The default is 5*kN.
    k : Material stiffness, optional
        Material stiffness. The default is 200*10**9.
    b : Post-yield stiffness, optional
        The stiffness of the nonlinear material after yielding. The default is 0.001.

    """ 
    
    ERelease = 1.
    
    # released material for diagnostic purposes only.
    op.uniaxialMaterial( 'Elastic' ,  2,  ERelease,  0.0 )
    
    # elastic material    
    op.uniaxialMaterial( 'Elastic' ,  10,  k,  0.0 )

    # NL material
    op.uniaxialMaterial( 'Steel02', 11,  Fu,  k, b, 18., .925, 0.15)
    
    ## Define geometric transformation(s) 
    ## ---------------------------------- 
    op.geomTransf('Linear',1) 
    # op.geomTransf('PDelta',1)
    op.beamIntegration('Lobatto', 1, 1, 3)



    
def buildTruss(Areas, NodeIds, xNodeCoords, yNodeCoords, Connectivity, 
               trussMat = 10):
    """
    Builds the truss model in OpenSeesPy.
    Assumes that the materials and sections have already been created.

    Parameters
    ----------
    Areas : list of float
        The are of each truss.
    NodeIds : list of int
        The ID of each node in the truss.
    xNodeCoords : list of float
        The x coordinate of each node in the truss.
    yNodeCoords : list of float
        The y coordinate of each node in the truss.
    Connectivity : list of list
        A list that contains element connectivity, in the from of node to node.
    trussMat : int, optional
        The material used for the truss. 10 is linear, 11 is a nonlinear material. 
        The default is 10.

    Returns
    -------
    Volumes: list
        The volume of each truss.

    """
        
    Volume = [0]*len(Areas)
    Nnodes = len(xNodeCoords)
    
    for ii in range(Nnodes):
        ID = int(NodeIds[ii])
        op.node(ID,  xNodeCoords[ii], yNodeCoords[ii],  '-ndf', 3)
        # op.node(2,  0., 0.,  '-ndf', 3)
        if ii == 0 or ii == 1:
            op.fix(ID,1,1,1)
        else:
            # op.fix(ID,1,1,1)
            op.fix(ID,0,0,1)
    tempL = 0.
    
    for ii, connect in enumerate(Connectivity):
        ID = int(ii + 1)
        op.element("truss " , ID  , int(connect[0]), int(connect[1]), Areas[ii], trussMat)
        
        p1 = np.array(op.nodeCoord(int(connect[0])))
        p2 = np.array(op.nodeCoord(int(connect[1])))
        
        tempL = (np.sum((p1 - p2)**2))**0.5
        
        Volume[ii] = Areas[ii]*tempL

    return np.array(Volume)


def applyLoads(Forces, Node=7):
    """
    Applied forces to the truss at an node arbitarily defined.
    The load will be applied across 10 timesteps.

    Parameters
    ----------
    Forces : list
        Forces in format [Fx, Fy, Mx].
    Node : int, optional
        The index of the node to apply forces to. The default is 7.

    """
    
    # Define a linear time series, we will apply the load in 10 steps.
    op.timeSeries('Linear', 1,'-factor' ,1.0)  
    op.pattern  ('Plain',1, 1,  '-fact', 1.) 
    op.load(Node, *Forces/10)
    # op.load(4, *Forces/10)
    



def defineBasicAnalysis():
    """
    Some adds some boiler plate settings for a typical laod controlled linear/nonlinear 
    analysis.

    """
                            
    op.constraints("Plain")
    op.numberer("Plain")
    # System of Equations 
    op.system('BandGen')
    # Convergence Test 
    op.test('NormDispIncr',  1.*10**-8, 25, 0 , 2)
    # Solution Algorithm 
    op.algorithm('Newton')
    # Integrator 
    op.integrator('LoadControl', 1, 1)
    # Analysis Type 
    op.analysis('Static')



def runTrussAnalysis(Areas, Forces, NodeIds, xNodeCoords, yNodeCoords, Connectivity, trussMat = 10, controlNode = 7):
    """
    Runs the analysis on our truss. Calls the functions defined prior.

    Parameters
    ----------
    Areas : list of float
        The are of each truss.
    NodeIds : list of int
        The ID of each node in the truss.
    xNodeCoords : list of float
        The x coordinate of each node in the truss.
    yNodeCoords : list of float
        The y coordinate of each node in the truss.
    Connectivity : list of list
        A list that contains element connectivity, in the from of node to node.
    trussMat : int, optional
        The material used for the truss. 10 is linear, 11 is a nonlinear material. 
        The default is 10.    
    controlNode : int, optional
        The index of the node to apply forces to. The default is 7.

    Returns
    -------
    disp : array
        The output displacement at the controll node in [ux, uy, uz].
    volume : array
        The volume of each truss, defined using the input areas and lengths.
    Forces : array
        The output forces in each truss.

    """
    
    # Make the model
    op.wipe()
    op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )

    # Define Element IDs
    Eles = range(len(Connectivity))

    # Define materials and geometry 
    # ---------------
    getSections()
    
    
    volume = buildTruss(Areas, NodeIds, xNodeCoords, yNodeCoords, Connectivity, trussMat)
    applyLoads(Forces, controlNode)
    
    # Define Analysis Parameters
    # ----------------- 
    defineBasicAnalysis()
    op.record()
    
    # Run the analysis, use 10 steps
    for ii in range(10):
        ok = op.analyze(1)
    
    # Run the analysis.
    disp = np.array(op.nodeDisp(controlNode))

    # Read the output Forces
    Forces = [None]*len(Eles)
    for ii in Eles:
        Forces[ii] = np.array(op.eleForce(int(ii + 1)))
    Forces = np.array(Forces)

    return disp, volume, Forces



# =============================================================================
# Misc.
# 
# =============================================================================

def plotTruss(Areas,NodeIds, xNodeCoords, yNodeCoords, Connectivity):
    """
    Displays a plot of the truss.

    Parameters
    ----------
    Areas : list of float
        The are of each truss.
    NodeIds : list of int
        The ID of each node in the truss.
    xNodeCoords : list of float
        The x coordinate of each node in the truss.
    yNodeCoords : list of float
        The y coordinate of each node in the truss.
    Connectivity : list of list
        A list that contains element connectivity, in the from of node to node.

    """
    
    op.wipe()
    op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )
    getSections()
    buildTruss(Areas,NodeIds, xNodeCoords, yNodeCoords, Connectivity)
    
    
    return opp.plot_model("nodes", "elements")
