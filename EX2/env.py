# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""

    
ExperimentStyle = {'linewidth':2, 'linestyle':'-','color':'C1'}
AnalysisStyle = {'linewidth':1, 'linestyle':'--','color':'C0'}


import openseespy.opensees as op
import numpy as np
import hysteresis.hys as hys

import os


class Environment:
    
    def __init__(self, llims, ulims):
        self.llims = llims
        self.ulims = ulims
        pass

    def testIndividual(self, individual):
        
        [Fu, k, b, R0, cR1, cR2] = individual.genome
        gen = str(individual.gen)
        name = str(individual.name)
        print(name)
            
        op.wipe()
        
        op.model('Basic' , '-ndm',  2,  '-ndf' , 3 )
        
        
        ## Analysis Parameters material(s) 
        ## ------------------
        LoadProtocol = np.array([0.00042, 0.0006, 0.0009, 0.0012, 0.0018, 0.0024, 
                                 0.0036, 0.0048, 0.0073, 0.010, 0.014, 0.019, 0.028, 
                                 0.04, 0.054, 0.07])
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
        op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'RFrc.out' , '-time' ,  '-nodeRange', 1,1, '-dof', 1,  2,  3 , 'reaction')
        op.recorder( 'Node' , '-file' , 'gen' + gen + '\\' + name + ' ' + 'Disp.out' , '-time' ,  '-nodeRange', 2,2, '-dof', 1,  2,  3 , 'disp')
        
        
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
                        return -1
                    
                op.integrator('DisplacementControl', ControlNode, ControlNodeDof, -dx)
                while (op.nodeDisp(2,1) > -x):
                    ok = op.analyze(1)
                    if ok != 0:
                        print('Ending analysis')
                        op.wipe()
                        return -1                  
                    
        op.wipe()    
        
        return 0
    
    def getGenone():
        pass
  
def initPopulation(genePool, size):
    """ Creates the first generation of the population"""
    gen = 0
    population = []
    for ii in range(size):
        genome = genePool.getGenome()
        population.append(Individual(genome))
    return population

      

# def getGene(llim, ulim, rand):
#     dx = ulim - llim
    
#     val = dx*rand + llim
    
#     return val

# def getGenome(llims, ulims):
    
#     Ngenes = len(llims)
#     rand = np.random.random(Ngenes)
#     genome = getGene(llims, ulims, rand)
    
#     return genome
    
    
# class Population:
    
#     def __init__(self):
#         pass
    

# def initPopulation(size, llims, ulims):
#     """ Creates the first generation of the population"""
#     gen = 0
#     population = []
#     for ii in range(size):
#         genome = getGenome(llims, ulims)
#         population.append(Individual(genome))
#     return population


    
class GenePool:
    
    # Generates valid solutions for each individual genom
    def __init__(self, llims, ulims):
        self.llims = llims
        self.ulims = ulims

    def getGene(self, rand):
        
        dx = self.ulims - self.llims
        gene = dx*rand + self.llims
        return gene
    
    def getGenome(self):
        Ngenes = len(self.llims)
        rand = np.random.random(Ngenes)
        genome = self.getGene(rand)
        
        return genome


class Individual:
    
    def __init__(self, genome):
        self.genome = genome
        
    def setname(self, name):
        self.name = name
    
    def setGen(self, gen):
        self.gen = gen
    
    def getxy(self):
        
        fileDispName = os.path.join('gen' + str(self.gen), str(self.name) + 'Disp.out')
        fileForceName = os.path.join('gen' + str(self.gen), str(self.name) + 'RFrc.out')
        
        disp = np.loadtxt(fileDispName)
        RFrc = np.loadtxt(fileForceName)
        
        # try:
        x = disp[:,1]
        y = -RFrc[:,1]
        
        xy = np.column_stack([x,y])
        return xy
    

    
def fitness(individual, hys2, jj):
    # Npoint = len(route)
    # Indexes = np.arange(Npoint)
    
    xyAnalysis = individual.getxy()
    
    hys1 = hys.Hysteresis(xyAnalysis)
    # hys2 = hys.Hysteresis(xyExp)
    
    try:
        diff, test = hys.CompareHys(hys1, hys2)
    except:
        diff  = 10**6
   
    return diff
    
def reNamePopulation(population, gen):
    
    for ii, individual in enumerate(population):
        individual.name = int(ii)
        individual.gen = int(gen)
    
def crossover(a, b):
    
    # This function allows us to generate two new solutions by swaping two
    # old solutions a and b.
    
    # The new solution is generated by finding a common point on the path bewtween
    # the two older solutions, then slicing the cunction at that point
    
    genomea = a.genome
    genomeb = b.genome
    Ngenes = len(genomea)
        
    aOut = np.zeros(Ngenes)
    bOut = np.zeros(Ngenes)
    
    # pick a random cut point
    cut = np.random.choice(np.arange(Ngenes))   
       
    # Concetenate makes a new object, no need for copies.
    aOut = np.concatenate([genomea[:cut], genomeb[cut:]])
    bOut = np.concatenate([genomeb[:cut], genomea[cut:]])
    
    return (Individual(aOut), Individual(bOut))

def mutate(individual, threshold, GenePool):
    
    #TODO:
        # maybe don't create a new genome?
    
    # for each value we randomly mutate depeding on the threshold.
    N = len(individual.genome)
    Pvector = np.random.random_sample(N)
    currentGenome = individual.genome
    tempGenome = GenePool.getGenome()
    
    # Find the first value less than the threshold
    mutateIndexes = np.where(Pvector < threshold)
    currentGenome[mutateIndexes] = tempGenome[mutateIndexes]
    individual.genome = currentGenome
    
    return individual

def score_population(population, environment, xyexp):
    # Find scores for every item of hte pupulation
    
    scores = []
    
    for ii in range(len(population)):
        score = fitness(population[ii], xyexp, ii)
        scores += [score]
        
    return np.array(scores)


def get_fitness_probailities(scores):
        # find wich scores should be combined
    # Scores with a low fitness should be combined at higher probability
    Npop = len(scores)   
    populationRanks = np.zeros(Npop)
    
    # sort the array, then create an array of ranks
    sortedIndexes = scores.argsort()    
    populationRanks[sortedIndexes] = np.arange(Npop)

    # the inverse of the fitness rank
    rankedFitness = Npop - populationRanks
    
    cumulativeFitness = np.cumsum(rankedFitness)
    probs = cumulativeFitness / cumulativeFitness[-1]
    
    return probs


def pick_mate(population, scores, probs):
    # Select a mamber of the pupulation at random depending on the ranked probability
    
    Nprobs = len(probs)
    rand = np.random.random()

    Mate = population[np.argmax(rand < probs)]
    return Mate



