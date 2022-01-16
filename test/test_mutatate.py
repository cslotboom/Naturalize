import naturalize.crossover.cross as c
import naturalize.crossover.cross as st
from naturalize.solutionClass import Individual
import numpy as np
import pytest





from naturalize.crossover import crossGene, defaultCrossover
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

    
    out1, out2 = crossGene(genea, geneb)
    
    check1 = np.all(genea[:4] == out1[:4]) and (geneb[4] == out2[4])
    check2 = np.all(geneb[:4] == out2[:4]) and (genea[4] == out1[4])
    
    assert np.all(check1 == check2)


def test_default_crossGene():

    
    Indout1, Indout2 = defaultCrossover(individualA, individualB)
    
    genea = individualA.genotype[0]
    geneb = individualB.genotype[0]
    
    out1 = Indout1.genotype[0]
    out2 = Indout2.genotype[0]
    
    check1 = np.all(genea[:2] == out1[:2]) and (geneb[2:] == out2[2:])
    check2 = np.all(geneb[:2] == out2[:2]) and (genea[2:] == out1[2:])
    
    assert np.all(check1 == check2)






test_crossGene()








# test_input_Parse_func()
# def test_default_crossGene():

#     solution1 = np.array([0,1,10,15,20,25])
#     solution2 = np.array([0,5, 2, 3, 4, 5])


#     crossover = st.getCrossover(0)

#     Indout1, Indout2 = crossover(individualA, individualB)
    
#     # genea = individualA.genotype[0]
#     # geneb = individualB.genotype[0]
    
#     out1 = Indout1.genotype[0]
#     out2 = Indout2.genotype[0]
    
#     check1 = np.all(out1 == solution1)
#     check2 = np.all(out2 == solution2)
    
#     assert check1== True and check2 == True


# test_default_crossGene()


