# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 22:59:59 2020

@author: Christian
"""


# function to be omptimzied

def optimizeFunction(x, y, z):
    
    result = x**2*y**5 + z
    
    return result


def ftest(individual, env):
    
    result = optimizeFunction(*individual.genotype)
    individual.result = result
    return result

def fitness(individual, Environment):
    
    """ In this case getting fitness from our result is trivial
    """
    
    fitness = individual.result
    return fitness
