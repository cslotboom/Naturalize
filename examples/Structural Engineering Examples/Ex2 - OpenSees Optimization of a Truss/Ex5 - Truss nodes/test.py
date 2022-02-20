# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import naturalize as test
import numpy as np
import sys
import TrussAnalysis as ta


from functions import environment


domain = [np.array([0,2]), np.array([0,4])]
domain = [np.array([0,2]), np.array([0,4])]
env = environment(11,domain)

assert env.dx == 2

Nodegenes = np.array([10, 50, 55, 5, 99, 23], int)
