
import naturalize.crossover.cross as c
import naturalize.crossover.cross as st
from naturalize.solutionClass import Individual
import numpy as np
import pytest

genea = np.linspace(0,5,6)
geneb = np.linspace(0,5,6)*5

individualA = Individual([genea])
individualB = Individual([geneb])


scores = np.array([0.1, 1, 5, 4,56, 5])
Npop = len(scores)

solution = np.array([0,1,3,2,5,4])


def custom_Crossover(geneA, geneB):
    
    return  np.zeros_like(geneA), np.zeros_like(geneB)





def test_input_Parse_int():
    strat = c._parseStrategyInputs(1)

    assert strat == st.crossGeneAvg


def test_input_Parse_int_fail():
    
    with pytest.raises(Exception):
        strat = st._parseStrategyInputs(4)

    # assert stat == 

def test_input_Parse_func():
    strat = c._parseStrategyInputs(custom_Crossover)

    assert strat == custom_Crossover

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


