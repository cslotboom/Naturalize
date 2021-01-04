# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as test
import numpy as np
import os
import hysteresis.hys as hys

import matplotlib.pyplot as plt
import openseespy.opensees as op

# function to be omptimzied

def testIndividual(individual):
    """
    Tests and individual and returns the result of that test.
    
    The user should consider if it's possible for the test not to work.
    
    """
    
    # Test outcomes:
    # The attempt at testing the individual did not work.
    
    # The test did work, and there is a score.
    
    [Fu, k, b, R0, cR1, cR2] = individual.genome
    gen = str(individual.gen)
    name = str(individual.name)
    print(name)    
    
    
    # Make a folder for the file.
    genName = 'gen' + str(int(gen))
    
    if not os.path.isdir(genName):
        os.mkdir(genName)

        
    op.wipe()
    
    op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )
    
    
    ## Analysis Parameters material(s) 
    ## ------------------
    LoadProtocol = np.array([0.0017, 0.005, 0.0075, 0.012, 0.018, 0.027, 
                             0.04, 0.054, 0.068, 0.072,0.])

    # Step size
    dx = 0.0001
        
    op.uniaxialMaterial( 'Steel02', 1,  Fu,  k, b, R0, cR1, cR2, 0.,  1.,  0.,  1.)
    
    ERelease = 1.
    op.uniaxialMaterial( 'Elastic' ,  2,  ERelease,  0.0 )
    
    ## Define geometric transformation(s) 
    ## ---------------------------------- 
    #geomTransf('Linear',1) 
    op.geomTransf('PDelta',1)
    op.beamIntegration('Lobatto',1,1,3)
    
    # Define geometry 
    # ---------------
    op.node(1,  0., 0.,  '-ndf', 3)
    op.node(2,  0., 0.,  '-ndf', 3)
    op.fix(1,1,1,1)
    
    # Define element(s) 
    # ----------------- 
    op.element("zeroLength" , 1  , 1, 2, '-mat', 1,2,2,'-dir', 1,2,3, '-orient', 1., 0., 0., 0., 1., 0.)
    

    # Define Recorder(s) 
    # ----------------- 
    op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'RFrc.out' , '-time' ,  '-nodeRange', 1,1, '-dof', 1 , 'reaction')
    op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'Disp.out' , '-time' ,  '-nodeRange', 2,2, '-dof', 1 , 'disp')
    
    
    # Define Analysis Parameters
    # ----------------- 
    op.timeSeries('Linear',1,'-factor' ,1.0)  
    op.pattern  ('Plain',1, 1,  '-fact', 1.) 
    op.load(2, 1.,  0.0, 0.0)
    
     
    # op.initialize() 
    op.constraints("Plain")
    op.numberer("Plain")
    # System of Equations 
    op.system("UmfPack", '-lvalueFact', 10)
    # Convergence Test 
    op.test('NormDispIncr',  1.*10**-8, 25, 0 , 2)
    # Solution Algorithm 
    op.algorithm('Newton')
    # Integrator 
    op.integrator('DisplacementControl', 2, 1, dx)
    # Analysis Type 
    op.analysis('Static')
    
    ControlNode = 2
    ControlNodeDof = 1
    
    op.record()
    
    ok = 0
    # Define Analysis 
    for x in LoadProtocol:
        for ii in range(0,1):
            
            # op.
            op.integrator('DisplacementControl', ControlNode, ControlNodeDof, dx)
            while (op.nodeDisp(2,1) < x):
                ok = op.analyze(1)
                if ok != 0:
                    print('Ending analysis')
                    op.wipe()
                    return np.array([0,0])
                
            op.integrator('DisplacementControl', ControlNode, ControlNodeDof, -dx)
            while (op.nodeDisp(2,1) > -x):
                ok = op.analyze(1)
                if ok != 0:
                    print('Ending analysis')
                    op.wipe()
                    return np.array([0,0])                  
                
    op.wipe()    
    
    fileDispName = os.path.join('gen' + str(gen), str(name) + 'Disp.out')
    fileForceName = os.path.join('gen' + str(gen), str(name) + 'RFrc.out')
    
    disp = np.loadtxt(fileDispName)
    RFrc = np.loadtxt(fileForceName)
    
    # try:
    x = disp[:,1]
    y = -RFrc[:,1]
    
    xy = np.column_stack([x,y])
    return xy

def ftest(individual):
    result = testIndividual(individual)
    individual.result = result
    return result

class Environment:
    
    def __init__(self):
        
        inches = 0.0254
        kip = 4.45*10**3
        
        EDataName = "BackboneData.csv"
        ExperimentData = np.loadtxt(EDataName,delimiter=',')
        
        Backbonex = ExperimentData[:,0]*inches
        Backboney = ExperimentData[:,1]*kip
        
        xyExp = np.column_stack([Backbonex, Backboney])
        self.hys2 = hys.Hysteresis(xyExp) 

def fitness(individual, environment):
    # Npoint = len(route)
    # Indexes = np.arange(Npoint)
    
    xyAnalysis = individual.result
    
    try:
        hys1 = hys.Hysteresis(xyAnalysis)
    except:
        return 10**6
    hys2 = environment.hys2


    try:
        diff, test = hys.CompareHys(hys1, hys2)
    except:
        diff  = 10**6
   
    return diff



np.random.seed(40)
llims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 0.
ulims =  np.array([21.1*10**3, 2.6*10**6, 0.015, 19, .95, .15]) * 1.5
genePool = test.DefaultGenePool(llims, ulims)
analysisEnvironment = Environment()

helper = test.AlgorithmHelper(ftest, fitness, genePool, environment = analysisEnvironment)

Ngen = 50
Npop = 30
Ncouples = 10
Nsurvive = 2
mutateThresold = 0.1

Analysis = test.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
Analysis.optimize()
test.pickleAnalysis(Analysis, 'OpenSees.obj')

# =============================================================================
# 
# =============================================================================

out = test.readPickle('OpenSees.obj')
fig, ax = plt.subplots()
# test.plotAvgFitness(fig, ax, out)
test.plotMinFitness(fig, ax, out)
test.plotTotalFitness(fig, ax, out)

