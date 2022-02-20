# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""
import hysteresis

import naturalize as test
import numpy as np
import sys
# import TrussAnalysis as ta
# np.random.seed(100)
import time
from functions import environment


# domain = [np.array([0,2]), np.array([0,4])]
# domain = [np.array([0,2]), np.array([0,4])]
# env = environment(11,domain)

# assert env.dx == 2

# Nodegenes = np.array([10, 50, 55, 5, 99, 23], int)

# =============================================================================
# Set up + test environment
# =============================================================================

pairs = []
Nnodes = 10
Nconnect = int(Nnodes*(Nnodes - 1) / 2)

Ngrid = 201
xlims = np.array([0,2])
ylims = np.array([0,2])
trussMat = 10       # can be 10 or 11
forces = np.array([1000., 1000., 0.])
# 

env = environment(Ngrid, xlims, ylims, trussMat, forces, Nnodes)

# print(env.connections)
# print(env.connections[0])

pairs = env.connections
# =============================================================================
# 
# =============================================================================

# removes a nodes
nodeMaskGene = np.random.randint(0,2,Nnodes,bool)

connectGene = np.random.randint(0,2,Nconnect,bool)

Nodes = np.linspace(1,Nnodes,Nnodes,dtype=int)
removeNodes = Nodes[nodeMaskGene]

# maskConnect = np.zeros(Nconnect)

# mapArray = np.ones([Nconnect, Nnodes ])


env.setConnectivityMatrix()
mapArray = env.connectMatrix
# print(env.connectMatrix)

# =============================================================================
# Approach 2 - generat the matrix using a mathmatical mapping.
# =============================================================================


# tempMapArray = np.zeros([Nconnect,Nnodes], dtype = bool)
# for ii, val in enumerate(nodeMaskGene):
#     if val == 1:
#         # tempMapArray[:,ii] = 1
#         tempMapArray[:,ii] = mapArray[:,ii]
#     else:
#         # tempMapArray[:,ii] = mapArray[:,ii]
#         tempMapArray[:,ii] = 1
        

# maskConnect = np.product(tempMapArray,1,dtype=bool)
# filConnect = connectGene*maskConnect

# connections = np.array(pairs[filConnect])

# print(connections)


con = env.getConncetivity(nodeMaskGene, connectGene)

print(con)


# =============================================================================
# 
# =============================================================================

# t1 = time.time()


# iterations = 1000*100
# for kk in range(iterations):
    
#     tempMapArray = np.zeros([Nconnect,Nnodes], dtype = bool)
#     for ii, val in enumerate(nodeMaskGene):
#         if val == 1:
#             # tempMapArray[:,ii] = 1
#             tempMapArray[:,ii] = mapArray[:,ii]
#         else:
#             # tempMapArray[:,ii] = mapArray[:,ii]
#             tempMapArray[:,ii] = 1
            
    
#     maskConnect = np.product(tempMapArray,1,dtype=bool)
#     filConnect = connectGene*maskConnect
    
#     possiblePairs = np.array(pairs[maskConnect])
# print(possiblePairs)
# t2 = time.time()
# print(t2-t1)



# =============================================================================
# Approach 1 - make the connectivity list by removing bad items
# =============================================================================



# t1 = time.time()

# # 
# iterations = 1000*100
# for ii in range(iterations):
#     outputPairs = []

#     for pair in pairs:
#         # outputPairs = []
#         check = False
#         for node in removeNodes:
#             # check = True
#             if node in set(pair):
#                 check = True
#                 break
#         if check == False:
#             pass
#             outputPairs.append(pair)

# print(outputPairs)
# t2 = time.time()
# print(t2-t1)
