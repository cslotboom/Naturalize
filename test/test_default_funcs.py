
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






# test_crossGene()
# test_default_crossGene()
# df.mutateGene()


# test_crossGene()

# print(out1, out2)
# helper = AlgorithmHelper()