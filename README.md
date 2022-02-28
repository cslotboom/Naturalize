
<p align="center">
  <img src="/doc/img/logo+text.jpg" alt="drawing" width="400"/>
</p>

<p align="center">
"From here, the world will be reborn."
</p>

Naturalize is a Python genetic algorithm solver for generic optimization problems. Given a function to solve and a set of "genes" that define the solution space, Naturalize can find solutions to arbitary problems. Naturalize provides users with many tools to customize their optimizaiton analysis, such as saving a particular generation and restarting the analysis. Naturalize also provides a set of tools for recording, tracking and visualizing genes over time.

Naturalize is in beta testing. This means that the solver is stable, but significant changes may occur to the function names or API. Use with caution. Comments are welcome!

## Getting started, basic example
In this basic example, the optimum value of a function will be found within a certain sets of bounds.
The output of the function will be minimized.

```Python 
import naturalize as nat

def objectiveFunction(x, y, z):
    """ The function we wish to minimize """
    return x*y + (z)

def ftest(individual, env):
    """ The function that will get applied to each individual. """
    individual.result = objectiveFunction(*individual.genotype[0])

lowerBounds = [-10, -10, -10]    # minimum values on each gene
upperBounds = [10, 10, 10]       # the maximum value on each gene
Ngen = 100              # Number of generations for the analysis
Npop = 30               # The population of each generaton
Ncouples = 10           # The number of couples - each makes two offspring
Nsurvive = 1            # The number of unmodified survivors

# Define the analysis objects.
genePool  = nat.BasicGenePool(lowerBounds, upperBounds)
helper    = nat.AlgorithmHelper(ftest, genePool)
algorithm = nat.GeneticAlgorithm(Npop, Ncouples, Nsurvive, helper)
analysis  = nat.Analysis(algorithm)
solution  = analysis.runAnalysis(Ngen)
print(solution)


```

## Examples of problems solved using Naturalize
Some examples of problems solved using naturalized are outlined in the examples. This includes:
Finding where to place nodes in a truss:
![Alt Text](https://github.com/cslotboom/Naturalize/blob/main/doc/img/Truss%20Optimization.gif)
Finding the correct position and colour of circles to draw a picture:
![Alt Text](https://github.com/cslotboom/Naturalize/blob/main/doc/img/Full%20Analysis.gif)

Detailed examples can be found in the examples folder. This includes:
 - solving basic Math equations (Ex 1.)
 - solving a travelling salesman problem (Ex 2.)
 - Calibrating the numerical mode of a siesmic damper (Structural Ex 1.)
 - Optimizing member sizes or node locations in a truss (Structural Ex 2.)

***

# How it works
Unlike many optimizaiton techniques, genetic algorithms require very little math to understand at a conceptual level. The optimization is completed by testing a number of solutions, or individuals, which each have a set of stored traits i.e. their genotype. As each individual is tested in a "generation", and from the tested individuals those with favorable traits are selected with some selection rule. The genes of these selected indivuduals are recombined through the process of 'crossover' and 'mutatation', leading to permutations of good solutions. The continuous change of genetic traights over time allows for the best solutions to be mantained and improved on.

# Algorithm Structure
Genetic algorithms are complete with the following basic operations

- Fitness testing
- Gene selection
- Mutation
- Crossover

Crossover is the process of. To parent individuals are selected using a, and have their genes randomly mixed. The thought being that if there are two favourable 

In naturalize we will specify:
- the gene pool
- 

Naturalize provides a class stucture for each of these


# Algorithm Structure
Naturalize provides the 

In naturalize we will specify:
- The population size
- The number of surivors
- The number of couples
- The probability of a mutation occuring.


# List of open questions:
As a work in pogress, there are some open technical questions that need to be solved, this includes:
- How to speed up the convergence for image matching? The convergence occurs very slowly for the final generations.

