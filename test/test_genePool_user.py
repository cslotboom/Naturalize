from naturalize.solutionClass import GenePool

import numpy as np
import pytest



def test_implementation():
    with pytest.raises(Exception):
        class NoInterface(GenePool):
            
            """
            A classs that doens't implement the interface.
            """
            
            pass
        NoInterface()
        
    # assert True
    
def test_implementation_passed():
    class Interface(GenePool):
        
        """
        A classs that does implement the interface.
        """
        def getNewGenotype(self):
            pass
    Interface()
    assert True == True
    

