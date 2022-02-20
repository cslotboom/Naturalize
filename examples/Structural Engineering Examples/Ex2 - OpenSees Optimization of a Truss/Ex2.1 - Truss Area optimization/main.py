# -*- coding: utf-8 -*-
"""
@author: CS

"""

"""
Import functions and set the random seed for reproducability.
"""
import naturalize as nat
import numpy as np
from functions import (ftest, fitness_basic, fitness_normalized, environment, 
                        plotIndividual)
# np.random.seed(40)
mm = 0.001


"""
Set the forces that will be applied to the problem.
"""
Forces = np.array([1000.,0.,0.])
env = environment(Forces)

"""
Set up the gene pool to be uniform between 0 and 100mm^2.

We'll use '
"""
llims =  np.ones(11)*0.
ulims =  np.ones(11) * 100. *mm**2
genePool = nat.BasicGenePool(llims, ulims)
helperBasic = nat.AlgorithmHelper(ftest, genePool, fitness_basic, environment = env)
helperNorm = nat.AlgorithmHelper(ftest, genePool, fitness_normalized, environment = env)

"""
Define population size. A fairly large sample size is used. We use a mutation
rate of about 1/N_gene.
"""

Ngen = 200
Npop = 50
Ncouples = 20
Nsurvive = 2
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



print(f'The best basic solution is: {best_basic*10**6} squre mm')

nat.plotAvgScore(data)
plotIndividual(best_basic)

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
fig, ax = plotIndividual(best_basic)
fig.set_figwidth(2)
fig.set_figheight(6)
# plt.rc('font', size=15) 
# fig.show()

for text in ax.texts:
    text.set_fontsize(10)
    
for ii, line in enumerate(ax.lines):
    line.set_linewidth(best_basic[ii]*10**6/10)
