
import naturalize.defaultFuncs as df
from naturalize.recorder import dataContainer
import numpy as np


recorder = dataContainer()


def test_init():

    assert(recorder.bestScores == [])


def test_append():

    recorder.bestScores.append(1)
    
    assert(recorder.bestScores == [1])

def test_convert():
    
    recorder.convert()
    
    check1 = np.all(recorder.bestScores== np.array([1]))
    check2 = isinstance(recorder.populations, np.ndarray)
    assert np.all([check1, check2])

# test_init()
# test_append()
# test_convert()



# test_crossGene()
# test_default_crossGene()
# df.mutateGene()


# test_crossGene()

# print(out1, out2)
# helper = AlgorithmHelper()