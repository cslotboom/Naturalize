
import naturalize.mutate.strategies as st
# from naturalize.solutionClass import Individual
import numpy as np

# np.random.seed(25)

N = 6
genea = np.linspace(0,5,N)
geneb = np.linspace(0,5,N)*5


Pvector = np.array([0.1, 0.1, 0.4, 0.5, 1, 0.1])
threshold = 0.2
bounds = np.ones([2,N])*np.array([[0,30]]).T
# purtThreshold = 0.1

def test_mutateGeneRandom():

    solution1 = np.array([0,5,2,3,4,25])
    out1 = st._mutateRandom(genea, geneb, threshold, Pvector,N)
     
    check1 = np.all(out1 == solution1)
    # check2 = np.all(out2 == solution2)
    
    assert check1== True

# test_mutateGeneRandom()

def test_mutateGenePereturbate_1():
    """
    This is a crude check right now because it doens't directly check the output,
    it only checks if it's within the expected bound.
    We do three checks to compensate for this
    """
    purtThreshold = 0.1
    out1 = st._mutatePerturbate(genea, threshold, Pvector, N, purtThreshold)
    check1 = np.sum(np.abs(out1  - genea)) < np.sum(purtThreshold*genea)
    # check2 = np.sum(out2  - solution2) < 0.0001
    
    assert check1== True


def test_mutateGenePereturbate_2():

    purtThreshold = 0.0000001
    out1 = st._mutatePerturbate(genea, threshold, Pvector, N, purtThreshold)
    check1 = np.sum(np.abs(out1  - genea)) < np.sum(purtThreshold*genea)
    # check2 = np.sum(out2  - solution2) < 0.0001
    
    assert check1== True

def test_mutateGenePereturbate_3():
    purtThreshold = 0.5
    out1 = st._mutatePerturbate(genea, threshold, Pvector, N, purtThreshold)
    check1 = np.sum(np.abs(out1  - genea)) < np.sum(purtThreshold*genea)
    # check2 = np.sum(out2  - solution2) < 0.0001
    
    assert check1== True


def test_EnforceBoundary():
    inArray = np.array([-1,-2,4,5,45,31])
    solution = np.array([0,0,4,5,30,30])
    bounds
    output = st._enforceBoundary(inArray, bounds)
    check1 = np.all(output == solution)
    
    
    
    assert check1 
    
# test_EnforceBoundary()


# test_mutateGenePereturbate_1()
# test_mutateGenePereturbate_2()
# test_mutateGenePereturbate_3()