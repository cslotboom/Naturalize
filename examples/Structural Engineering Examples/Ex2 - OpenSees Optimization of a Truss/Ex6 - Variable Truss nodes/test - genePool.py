

import numpy as np
from functions import genePool


Ngrid = 201

Nmax = Ngrid**2 - 1

Nnodes = 5
Nconnect = int(Nnodes*(Nnodes - 1) / 2)
staticNodes = np.array([100,100], int)




lNodeCoords = np.zeros(Nnodes)
uNodeCoords = np.ones(Nnodes)*Nmax

lnodeMask = np.zeros(Nnodes)
uNodeMask = np.ones(Nnodes)*2

lconnectMask = np.zeros(Nconnect)
uconnectMask= np.ones(Nconnect)*2

llims = [lNodeCoords, lNodeCoords, lconnectMask]
ulims = [uNodeCoords, uNodeMask, uconnectMask]

pool = genePool(llims, ulims)
pool.setStaticNodes(staticNodes)

test1 = pool.getGenotype()


# pool = genePool(llims, ulims)

# Define set the algorithm helper
# helper = nat.AlgorithmHelper(ftest, fitness, pool, environment = env)

# GenePool