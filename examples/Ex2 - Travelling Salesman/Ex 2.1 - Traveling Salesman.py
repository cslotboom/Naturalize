# -*- coding: utf-8 -*-
"""
@author: Christian

An example that solves a traveling salesman problem via. genetic algorithm.
Example has been adapted from Greg Michaelson's examples here:
    https://github.com/gmichaelson/GA_in_python
    https://www.youtube.com/channel/UCnE8sAcJ-x1ttDcYPqoAdOg


It's important to first understand the traveling salesman problem. A series
of nodes are connected, each with a "distance" betwen them.
THe goal will be to find the smallest path between a start node "A" and end 
node "B".

A map is first defined that represents the connection between a set of nodes.
In this problem the mapping is defined randomly, such that each node has a 
random chance of being connected to each other node.
This problem defines custom functions to solve the system.
"""

"""
Import the solution functions - see defintion in the functions folder.
"""

import numpy as np
import naturalize as nat
from functions import Environment, myGenePool, ftest, fitness, crossover, mutate, plot_best, plot_map
np.random.seed(40)

"""
Define the graph. This is defined by a set of nodes and a connectivity matrix.
The connectivity matrix , as well as a distance to the other nodes.
"""
sparseness_of_map = 0.5  # The probability each node is connected to other nodes
size_of_map = 1000  # The total number of nodes
number_of_iterations = 1000
mutation_probability = 0.01
env = Environment(sparseness_of_map, size_of_map)

"""
A image of the mapping matrix can be plotted with the functions we defined.
The distance between each node is depicted with colour, and 0 distance means
the nodes are not connected.
"""

plot_map(env.mapping)

"""
Start and end node, chosen arbitrarily. Note, it's possible to choose two
disconnected end nodes, the values of the above problem are chosen so that 
this will not happen.
"""

startNode = 60
endNode = 520
genePool = myGenePool(startNode, endNode, env.mapping)
helper = nat.AlgorithmHelper(ftest, genePool, fitness, mutate, crossover, environment=env)

Ngen = 40
Npop = 40
Ncouples = 8
Nsurvive = 2
mutateThresold = 0.1

algorithm = nat.GeneticAlgorithm(helper, Ngen, Npop, Ncouples, Nsurvive, mutateThresold)
analysis  = nat.Analysis(algorithm)
solution  = analysis.runAnalysis(Ngen)

plot_best(genePool.mapping, solution, Ngen, startNode, endNode)

