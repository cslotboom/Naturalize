
import naturalize.defaultFuncs as df
from naturalize.solutionClass import Individual
import numpy as np

np.random.seed(25)

# df.defaultFitness(individual, env)
genea = np.empty(5)
geneb = np.empty(5)

individualA = Individual([genea])
individualB = Individual([geneb])
# genea = np.array([1,1,1,1,1,0])
# geneb = np.array([1,2,2,2,2,1])

scores = np.array([0.1, 1, 5, 4,56, 5])
Npop = len(scores)

solution = np.array([0,1,3,2,5,4])

def test_crossGene():

    
    out1, out2 = df.crossGene(genea, geneb)
    
    check1 = np.all(genea[:4] == out1[:4]) and (geneb[4] == out2[4])
    check2 = np.all(geneb[:4] == out2[:4]) and (genea[4] == out1[4])
    
    assert np.all(check1 == check2)


def test_default_crossGene():

    
    Indout1, Indout2 = df.defaultCrossover(individualA, individualB)
    
    genea = individualA.genotype[0]
    geneb = individualB.genotype[0]
    
    out1 = Indout1.genotype[0]
    out2 = Indout2.genotype[0]
    
    check1 = np.all(genea[:2] == out1[:2]) and (geneb[2:] == out2[2:])
    check2 = np.all(geneb[:2] == out2[:2]) and (genea[2:] == out1[2:])
    
    assert np.all(check1 == check2)

# rankedFitness = _rankFitness(scores)

def test_rankScore():
    ranks = df._rankFitness(scores, Npop)
    assert np.all(solution == ranks)


def test_FitnessProbs():
    
    probs = df.defaultFitnessProbs(scores)
    
    sol = np.array([0.28571429, 0.52380952, 0.66666667, 0.85714286, 0.9047619 ,  1.])
    
    diff = np.sum(probs - sol)
    
    assert diff < 0.0001



# test_rankScore()



# test_FitnessProbs()

# test_crossGene()
# test_default_crossGene()
# df.mutateGene()


# test_crossGene()

# print(out1, out2)
# helper = AlgorithmHelper()