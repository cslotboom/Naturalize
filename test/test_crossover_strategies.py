
import naturalize.crossover.strategies as st
# from naturalize.solutionClass import Individual
import numpy as np

# np.random.seed(25)


genea = np.linspace(0,5,6)
geneb = np.linspace(0,5,6)*5


def test_crossGeneSingleCut():

    cut = 2
    solution1 = np.array([0,1,10,15,20,25])
    solution2 = np.array([0,5, 2, 3, 4, 5])
    out1, out2 = st._crossGeneSingleCut(genea, geneb, cut)
     
    check1 = np.all(out1 == solution1)
    check2 = np.all(out2 == solution2)
    
    assert check1== True and check2 == True

def test_crossGeneAvgSingleCut():

    cut = 2
    solution1 = np.array([0,1,6,9,12,15])
    solution2 = np.array([0,5,6,9,12,15])
    out1, out2 = st._crossGeneAvgSingleCut(genea, geneb, cut)
     
    check1 = np.sum(out1  - solution1) < 0.0001
    check2 = np.sum(out2  - solution2) < 0.0001
    
    assert check1== True and check2 == True

# test_crossGeneSingleCut()
# test_crossGeneAvgSingleCut()
