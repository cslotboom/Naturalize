
import naturalize as nat

import naturalize.crossover.strategies as st
from naturalize.solutionClass import Individual
import numpy as np
import pytest


llims = [[0,0,0],1,[3,4]]
ulims = [[1,1,7],6,[5,5]]


pool = nat.BasicGenePool(llims, ulims)

def test_Basic_for_array():

    test = pool.getNewGenotype()
    
    check = []
    for item in test:
        check.append(isinstance(item, np.ndarray))
        
    assert np.all(check ==[True,True,True])
    
test_Basic_for_array()

