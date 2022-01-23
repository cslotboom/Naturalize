
import naturalize.crossover.strategies as st
import naturalize.crossover.core as c
import naturalize as nat
import numpy as np

genea = np.linspace(0,5,6)
geneb = np.linspace(0,5,6)*5


def test_crossGeneSingleCut():

    cut = 2
    solution1 = np.array([0,1,10,15,20,25])
    solution2 = np.array([0,5, 2, 3, 4, 5])
    out1, out2 = st._crossGeneSingleCut(genea, geneb, cut)
     
    check1 = np.sum(out1  - solution1) < 0.0001
    check2 = np.sum(out2  - solution2) < 0.0001
    print(out1)
    assert check1== True
    # assert check1== True and check2 == True

def test_crossGeneAvgSingleCut():

    cut = 2
    solution1 = np.array([0,1,6,9,12,15])
    solution2 = np.array([0,5,6,9,12,15])
    out1, out2 = st._crossGeneAvgSingleCut(genea, geneb, cut)
     
    check1 = np.sum(out1  - solution1) < 0.0001
    check2 = np.sum(out2  - solution2) < 0.0001
    
    assert check1== True and check2 == True


test_crossGeneSingleCut()
test_crossGeneAvgSingleCut()


genec = np.empty(5)
gened = np.empty(5)

individualA = nat.Individual([genec])
individualB = nat.Individual([gened])


def test_crossGene():

    
    out1, out2 = st.crossGeneSingleCut(genec, gened)
    
    check1 = np.all(genec[:4] == out1[:4]) and (gened[4] == out2[4])
    check2 = np.all(gened[:4] == out2[:4]) and (genec[4] == out1[4])
    
    assert np.all(check1 == check2)


def test_default_crossGene():

    defaultCrossover = c.getCrossover()
    Indout1, Indout2 = defaultCrossover(individualA, individualB)
    
    genea = individualA.genotype[0]
    geneb = individualB.genotype[0]
    
    out1 = Indout1.genotype[0]
    out2 = Indout2.genotype[0]
    
    check1 = np.all(genec[:2] == out1[:2]) and (gened[2:] == out2[2:])
    check2 = np.all(gened[:2] == out2[:2]) and (genec[2:] == out1[2:])
    
    assert np.all(check1 == check2)


# test_crossGene()
# test_default_crossGene()