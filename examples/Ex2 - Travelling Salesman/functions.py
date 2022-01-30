# -*- coding: utf-8 -*-
"""
@author: Christian


An example that solves a traveling salesman problem via. genetic algorithm.
Example has been adapted from Greg Michaelson's examples here:
    https://github.com/gmichaelson/GA_in_python
    https://www.youtube.com/channel/UCnE8sAcJ-x1ttDcYPqoAdOg

A map is first defined that represents the connection between a set of nodes.
In this problem the mapping is defined randomly, such that each node has a 
random chance of being connected to each other node.

This problem defines custom functions to solve the system.


"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from naturalize.solutionClass import Individual, GenePool

# np.random.seed(4)
class Environment:
    
    def __init__(self, pZero, N):
        
        """
        First initialize the mapping that represents the input graph.
        Each row and column corresponds to an intersection on our map.
        A zero means that there is no connection.
        A Xij value means it takes X time to get fromm node i to node j
        
        """
        # Create a symetrical connectivity matrix
        tempArray = np.random.random([N,N])
        np.fill_diagonal(tempArray,0)
        mapping = (tempArray + tempArray.T) / 2
           
        # get the values less than our threshold probaility
        indexes = np.where(mapping < pZero )
        
        # scale up the numbers sysmetrically
        tempArray = np.random.random([N,N])*5
        mapping = mapping*(tempArray + tempArray.T) 
    
        mapping[indexes] = 0
        self.mapping = mapping
        

    
    
    
    
class myGenePool(GenePool):
    
    """
    A custome gene pool is defined. Recal the gene pool is what's used to 
    generate valid solutions. In this case, valid solutions are paths through
    the mapping.
    
    This is acompished by doing a random walk - a new node is randomly selected
    from the possible set of new nodes. 


    The getNewGenotype method is our interface. This must be implemented to
    work with the algoritm.    
    """
    
    # Generates valid solutions for each individual genom
    def __init__(self, start, end, mapping):
        self.start = start
        self.end = end
        self.mapping = mapping

    def getNewGenotype(self):
        return self.genereateValidRoute(self.start, self.end)
            
        
    def genereateValidRoute(self, start, end):
        # This assumes that there is a valid solution! There might not be one.

        mapping = self.mapping       
        
        # Do a random walk through the network, check if the next node is the end node
        go = True
        currentNode = start
        solution = [currentNode]
        
        while go == True:
            currentNodeMap = mapping[currentNode] 
            connectedNodeIndex = np.where(currentNodeMap != 0)[0]
            nextNode = np.random.choice(connectedNodeIndex)            
            solution.append(nextNode)
            
            
            if  nextNode == end:
                go = False
            currentNode = nextNode
            
        return np.array(solution)
    

def ftest(individual, environment):
    """
    The test function passes the individual through the environment and returns
    a result. In this case, the distance of the path is calcualted and summed.

    """
    
    # initialize some variables.
    mapping = environment.mapping
    route = individual.genotype
    Npoint = len(route)

    
    # Get the nodes that the rout takes. route entry
    startInd = np.arange(Npoint)
    startNodes = route[:-1]
    endInd = startInd[:-1] + 1
    endNodes = route[endInd]
    
    # Find the distances using the connectivity matrix
    # distances = mapping[route[:-1], shiftedRoute]
    dist = np.sum(mapping[startNodes, endNodes])
    
    return dist
    

def fitness(individual, Environment):
    
    """ 
    In this case getting fitness from our result is trivial
    """
    
    fitness = individual.result
    return fitness


def crossover(a, b):
    """
    The crossover is used to generate new solutions based on the two selected
    individuals. 
    In this case, new routes are found by finding common Nodes between each
    route, and swaping the parts of the solution at those points, i.e.
    
    start -> A -> D -> E -> J -> F -> End
    start -> E -> G -> End
    
    new solutions
    start -> A -> D -> E -> G -> End 
    start -> E -> J -> F -> End
    
    Outputs must be Individuals.
    
    """
            
    g1 = a.genotype
    g2 = b.genotype
    
    common_elements = set(g1[1:-1]) & set(g2[1:-1])
    
    g1Out = np.zeros_like(g1)
    g2Out = np.zeros_like(g2)
    
    # Output solution must have a common node, otherwise no crossover can be 
    # complete.
    if len(common_elements) == 0:
        return (a, b)
    
    # complete.
    value = np.random.choice(list(common_elements))   
    
    # Get the first cut value
    cutA = np.random.choice(np.where(g1 == value)[0])
    cutB = np.random.choice(np.where(g1 == value)[0])
    
    # return the output solutions.
    g1Out = np.concatenate([g1[:cutA], g2[cutB:]])
    g2Out = np.concatenate([g2[:cutB], g1[cutA:]])
    
    return (Individual(g1Out), Individual(g2Out))


def mutate(individual, threshold, genePool):
    """
    Mutates a solution by picking a random point along the solution, and 
    generating a new valid path from that point onwards.
    
    Mutations will depend on a threshold, which is between 0 and 1. This 
    roughly translates to the likihood of a mutation occuring in each gene.
    """
    route = individual.genotype
    N = len(route)
    
    # Find the first value less than the threshold
    Pvector = np.random.random_sample(N)
    cutIndex = np.argmin(threshold < Pvector)
    cutNode = route[cutIndex]
    
    # generate a new route        
    newTail = genePool.genereateValidRoute(cutNode, genePool.end)
    newGenotype = np.concatenate([route[:cutIndex], newTail])
    
    return Individual(newGenotype)
    


def plot_map(mapping):
    """
    A plot function to visualize the mapping
    """
    ax = sns.heatmap(mapping)
    plt.show()

def plot_best(mapping, route, iteration_number, start, end):
    """
    A plot function to visualize the mapping and solution.
    """
    ax = sns.heatmap(mapping)

    figsize = len(mapping)
    
    x=[start + 0.5] + [x + 0.5 for x in route[0:len(route)-1]] + [end - 0.5]
    y=[start + 0.5] + [x + 0.5 for x in route[1:len(route)]] + [end - 0.5]
    
    plt.plot(x, y, marker = 'o', linewidth=4, markersize=12, linestyle = "-", color='white')
    # plt.savefig('images/new1000plot_%i.png' %(iteration_number), dpi=300)
    plt.show()






