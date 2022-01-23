import naturalize.fitness as f
from naturalize.solutionClass import Individual
import numpy as np

scores = np.array([0.1, 1, 5, 4,56, 5])
Npop = len(scores)

solution = np.array([0,1,3,2,5,4])



def test_rankScore():
    ranks = f.rankFitness(scores, Npop)
    assert np.all(solution == ranks)


def test_FitnessProbs():
    
    probs = f.rouletteFitnessProbs(scores)
    
    sol = np.array([0.28571429, 0.52380952, 0.66666667, 0.85714286, 0.9047619 ,  1.])
    
    diff = np.sum(probs - sol)
    
    assert diff < 0.0001



# test_rankScore()
# test_FitnessProbs()
