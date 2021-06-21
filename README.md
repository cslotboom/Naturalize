# Naturalize
"From here, the world will be reborn."

Naturalize is a Python genetic algorithm solver for generic optimization problems. Given a function to solve and a set of "genes" that define the solution space, Naturalize can find solutions to arbitary problems. Naturalize provides users with many tools to customize their optimizaiton analysis, such as saving a particular generation and restarting the analysis their. Naturalize also provides a set of tools for tracking and visualizing genes over time.

Naturalize is in beta testing. This means that the solver is stable, but significant changes may occur to the function names or API. Comments welcome!

# List of open questions:
- How to speed up the convergence for image matching? The convergence occurs very slowly for the final generations.

# Examples of problems solved using Naturalize
Math equations (Ex 1.)
Travelling salesman problem (Ex 2.)
Calibrating the numerical mode of a siesmic damper (Ex 3.)
Optimizing member sizes in a truss (Ex 4.)
Topology optimziation for a truss structural system (Ex 5., Ex 6.)
Matching an image (Ex 7., Ex 8.)

# GIF

# How it works
Unlike many optimizaiton techniques, genetic algorithms require very little math to understand. The optimization is completed by testing a number of solutions, or individuals, which each have a set of different traits, i.e. their genotype. As each individual is tested, those with favorable traits will be more likely to reproduce and pass their genes to the next roung of solutions.

through the process of crossover and mutatation, good solutions are mantained and improved on.

Genetic algorithms are complete with the following basic operations

- Mutation
- Crossover

Crossover is the process of. To parent individuals are selected using a, and have their genes randomly mixed. The thought being that if there are two favourable 

In naturalize we will specify:
- the gene pool
- 



In naturalize we will specify:
- The population size
- The number of surivors
- The number of couples
- The probability of a mutation occuring.


# Example Basic
Finding the optimal values to a mathematical function:

Our test funciton will just be the equation we wanted to solve.

We can encode the as a set of numbers



# Basic Theory
