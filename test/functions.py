# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


import numpy as np
import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# function to be omptimzied

def optimizeFunction(x, y, z):
    
    result = x*y + (z)
    
    return result


def ftest(individual, env):
    # print(individual.genotype[0])
    
    result = optimizeFunction(*individual.genotype[0])
    individual.result = result
    return result

def fitness(individual, Environment):
    
    """ In this case getting fitness from our result is trivial
    """
    
    fitness = individual.result
    return fitness
