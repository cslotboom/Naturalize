
<p align="center">
  <img src="/doc/img/logo+text.jpg" alt="drawing" width="400"/>
</p>

<p align="center">
"From here, the world will be reborn."
</p>

Naturalize is a Python genetic algorithm solver for generic optimization problems. Given a function to solve and a set of "genes" that define the solution space, Naturalize can find solutions to arbitary problems. Naturalize provides users with many tools to customize their optimizaiton analysis, such as saving a particular generation and restarting the analysis. Naturalize also provides a set of tools for recording, tracking and visualizing genes over time.

Naturalize is in beta testing. This means that the solver is stable, but significant changes may occur to the function names or API. Comments welcome!

## Getting started, basic example
In this basic example.
Finding the optimal values to a mathematical function:

Our test funciton will just be the equation we wanted to solve.

We can encode the as a set of numbers


XXX code block for EX1



## Examples of problems solved using Naturalize
XXXX future gifs XXXX

Math equations (Ex 1.)
Travelling salesman problem (Ex 2.)
Calibrating the numerical mode of a siesmic damper (Ex 3.)
Optimizing member sizes in a truss (Ex 4.)
Topology optimziation for a truss structural system (Ex 5., Ex 6.)
Matching an image (Ex 7., Ex 8.)

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

