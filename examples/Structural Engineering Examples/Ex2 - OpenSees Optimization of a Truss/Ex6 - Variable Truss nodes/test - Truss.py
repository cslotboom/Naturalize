

import numpy as np
import openseespy.opensees as op

from functions import genePool, environment, plotIndividual, testIndividual
import sys
sys.path.append(r'C:\Users\Christian\Scripts\CodingAdventures\GeneticAlgorithms\Package')
import TrussAnalysis as ta
import naturalize as nat
np.random.seed(30)

Ngrid = 201

Nmax = Ngrid**2 - 1

Nnodes = 8
Nconnect = int(Nnodes*(Nnodes - 1) / 2)
staticNodes = np.array([100,200, Nmax - 1], int)

"""
gene1: position vector
gene2: Connectivity vector
gene3: Node Mask

"""    


lNodeCoords = np.zeros(Nnodes)
uNodeCoords = np.ones(Nnodes)*Nmax

lconnectMask = np.zeros(Nconnect)
uconnectMask= np.ones(Nconnect)*2

lnodeMask = np.zeros(Nnodes)
uNodeMask = np.ones(Nnodes)*2


llims = [lNodeCoords, lconnectMask, lnodeMask]
ulims = [uNodeCoords, uconnectMask, uNodeMask]

pool = genePool(llims, ulims)
pool.setStaticNodes(staticNodes)

individual = nat.Individual(pool.getGenotype())

pairs = []
# Nnodes = 10
Nconnect = int(Nnodes*(Nnodes - 1) / 2)

Ngrid = 201
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([1000., 1000., 0.])

env = environment(Ngrid, xlims, ylims, trussMat, forces, Nnodes, len(staticNodes))

# plotIndividual(individual, env)
# out = testIndividual(individual, env)
# op.eleForce(1)
# op.eleLoad()
# op.nodeDOFs()

# individual = nat.Individual(pool.getGenotype())
# plotIndividual(individual, env)
# out = testIndividual(individual, env)


# genotype = [np.array([  100,   200, 40399,  4180, 14733,  1597, 39118,  7997]),
#             np.ones(Nnodes, dtype=bool),
#             np.ones(Nconnect,dtype = bool)]




# =============================================================================
# 8Node test
# =============================================================================

# genotype = [np.array([  100,   200, 40399,  4180, 14733,  1597, 39118,  7997]),
#             np.ones(Nconnect, dtype=bool),
#             np.ones(Nnodes,dtype = bool)]
# genotype[2][4] = False
# genotype[2][5] = False
# # temp  =np.ones(Nconnect,dtype = bool)
# # genotype[2] = env.getConncetivity(genotype[1], temp)

# individual = nat.Individual(genotype)
# plotIndividual(individual, env)
# out = testIndividual(individual, env)



# =============================================================================
# 
# =============================================================================

ii = 0
disp = [1,1,1]
disps = np.zeros(10)
for ii in range(10):
    if ii == 1:
        pause = True
    individual = nat.Individual(pool.getGenotype())
    disp, _ = testIndividual(individual, env)
    if np.sum(disp) < 1:
        
        disps[ii] = np.sum(disp)
        plotIndividual(individual, env)
    
    
    
    
    
    
    
    
    
    
    
# while 1 < np.sum(disp):
#     if ii == 21:
#         pause = True
#     individual = nat.Individual(pool.getGenotype())
#     disp, _ = testIndividual(individual, env)
#     if np.sum(disp) < 1:
#         plotIndividual(individual, env)
#         end = ii
#     ii +=1











# pool = genePool(llims, ulims)

# Define set the algorithm helper
# helper = nat.AlgorithmHelper(ftest, fitness, pool, environment = env)

# GenePool