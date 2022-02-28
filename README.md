
<p align="center">
  <img src="/doc/img/logo+text.jpg" alt="drawing" width="400"/>
</p>

<p align="center">
"From here, let the world will be reborn."
</p>


Naturalize is a customizable Python framework for solving problems using genetic algorithms. Given a function to solve and a set of "genes" that define the solution space, Naturalize can find solutions to arbitary problems.  Naturalize provides users with many tools to customize their optimizaiton analysis, such as saving a particular generation and restarting the analysis. It also provides a set of tools for recording, tracking and visualizing genes over time, and allows users to  to write their own mutation, crossover, or selection functions.

Naturalize is in beta testing. This means that the solver is stable, but significant changes may occur to the function names or API. Use with caution. Comments are welcome!

## Getting Started: A Basic Example
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

## Examples of Problems Solved using Naturalize
Some examples of problems solved using naturalized are outlined in the examples. This includes:

Finding where to place nodes in a laterally loaded truss:
<p align="center">
    <img src="https://github.com/cslotboom/Naturalize/blob/main/doc/img/Truss%20Optimization.gif"/>
</p>

Finding the correct position and colour of circles to draw a picture:
<p align="center">
    <img src="https://github.com/cslotboom/Naturalize/blob/main/doc/img/Full%20Analysis.gif"/>
</p>

Detailed examples can be found in the examples folder. This includes:
 - solving basic Math equations (Ex 1.)
 - solving a travelling salesman problem (Ex 2.)
 - Calibrating the numerical mode of a siesmic damper (Structural Ex 1.)
 - Optimizing member sizes or node locations in a truss (Structural Ex 2.)

***

# How it Works
Genetic algorithms are an optimization technique where information about a possible solution, often termed "individual", is encoded in a set parameters that define that solution, often termed "genes". As with any optimization technique, the goal is to find a good solution to a input problem. The optimization occurs over a series of "generations", where in each generation a series of individual is tested, and the genes of successful individuals are used to define the new set of solutions in the next generation. The presevation and rearrangement of genetic traights over time allows for the best solutions to be mantained and improved on.

As the name suggests, genetic algorithms parallel evolution in nature, and many of the principles that apply to evolution also apply to genetic algorithms. Important aspects of this process includes: 
	• Selection, how individuals are chosen to pair off.
	• Crossover: how genetic information from the pair of selected solutions are mixed.
	• Mutation: how imperfection is introduced to selected solution between generations. 

When comparing genetic algorithms to other optimization techniques, there are a few thing to consider. Genetic algorithms tend to be slow at finding global optimal solutions compared derivative based optimization methods, such as gradient descent. However, genetic algorithms are also very adaptable. They can quickly find "good enough" solutions in situations where other algorithms struggle. They also only require information about the input parameters and output results, so they can be used in many "black-box" optimization problems. Genetic algorithms are also appealing because they are very easy to understand conceptually.

# Checklist for a Typical Problem
For a typical problem the following will need to be chosen:
- A solution space, including a gene structure to encode parameters and a gene pool that stores those parameters.
- A test funciton for the potential solutions
- A environment for data each individual needs access to
- A rule for mutating solutions between generations
- A rule for crossing over genes between generations.
- A rule for selecting sucessful solutions
