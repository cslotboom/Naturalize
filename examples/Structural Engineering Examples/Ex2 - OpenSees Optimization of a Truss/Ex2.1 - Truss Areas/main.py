# -*- coding: utf-8 -*-
"""
@author: CS

"""

"""
Import functions and set the random seed for reproducability.
"""
import naturalize as nat
import numpy as np
from functions import (ftest, fitness_basic, fitness_normalized, fitness_Volume, environment, 
                        plotIndividual)
import matplotlib.pyplot as plt

# np.random.seed(40)
mm = 0.001
kN = 1000
basicOutputData = 'Basic analysis data.P'
normOutputData = 'Normalized analysis data.P'

"""
Set the forces that will be applied to the problem.
"""
Forces = np.array([10*kN,0.,0.])
env = environment(Forces)

"""
Set up the gene pool to be uniform between 0 and 100mm^2.


"""
llims =  np.ones(11)*0.
ulims =  np.ones(11) * 100. *mm**2
genePool = nat.BasicGenePool(llims, ulims)
helperBasic = nat.AlgorithmHelper(ftest, genePool, fitness_basic, environment = env)
helperNorm = nat.AlgorithmHelper(ftest, genePool, fitness_Volume, environment = env)

"""
Define population size. A fairly large sample size is used. We use a mutation
rate of about 1/N_gene.
"""

Ngen = 1000
Npop = 50
Ncouples = 20
Nsurvive = 1
mutateThresold = 0.1

"""
The analysis will be run twice, one for each test funciton.
It's expcted that the basic function will trend towards, while the normalized
funciton will pick truss areas where stiffness is the most impactful.
"""

"""
Define the algorithm, analysis, and a recoder.
"""
algorithm = nat.GeneticAlgorithm(helperBasic, Npop, Ncouples, Nsurvive, mutateThresold)
recorder = nat.basicRecorder(5, 1)
analysisBasic = nat.Analysis(algorithm, recorder)

"""
Run the analysis and get the output data.
"""
best_basic = analysisBasic.runAnalysis(Ngen)
data = analysisBasic.getRecorderData()

nat.pickleData(data, basicOutputData)


# print(f'The best basic solution is: {best_basic*10**6} squre mm')

nat.plotAvgScore(data)












# =============================================================================
# Normalized analysis
# =============================================================================

"""
Define the algorithm, analysis, and a recoder.
"""
algorithm2 = nat.GeneticAlgorithm(helperNorm, Npop, Ncouples, Nsurvive, mutateThresold)
recorder = nat.basicRecorder(5, 1)
analysisNorm = nat.Analysis(algorithm2, recorder)

"""
Run the analysis and get the output data.
"""
best_basic = analysisNorm.runAnalysis(Ngen)
data = analysisNorm.getRecorderData()


print(f'The best normalized solution is: {best_basic*10**6} squre mm')

nat.plotAvgScore(data)

nat.pickleData(data, normOutputData)
  
    
for idv in data.bestIndividuals:
    print(idv.result[0][0])
    
    
    
    
    
    
    
    
