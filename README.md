# Ecoilogy

A genetic algorithm (GA) designed to optimize coil design according to axial field homogeneity.


### Important general definitions:
__Population:__ A group of individuals, where individuals are referring to individual coils.

__Coil:__ A group of wire loops. Can be also referred to as an "individual" according to the evolutionary analogy. Each individual is conceptually structured around its genetic material, which is to be manipulated by the GA.

__Loop:__ An ideal loop of wire, coaxial with the z-axis.

__Genetic Material:__ The z-positions and currents associated with all the loops in a coil.

__Chromosomes:__ Exactly one half of the genetic material. Each chromosome specifically refers to the z-position and current of a single loop within a coil. Since all coils this program deals with are symmetric, it is sometimes sufficient to deal with only the positive values of the loop positions, along with their corresponding currents.

__Genotype:__ The sum total of the genetic material. The loops on both the positive and negative z-axis, as well as their corresponding currents.


### Important algorithm-specific definitions:
__Parent Fraction:__ The fraction of the total population selected to be parents, according to their superior fitness.

__Lucky Probability:__ The chance that some of the less fit amongst the population will become parents. This has the purpose of maintaining genetic diversity within a population, to help avoid local minima.

__Mutation Probability:__ The chance that a given chromosome within a coil will be mutated. This is currently being treated as 1.

__(z or I) epsilon:__ Once a chromosome has been selected for mutation, this is the upper bound for the range from which perturbations will be chosen to mutate the chromosome.



The only file which should be modified to alter evolutionary performance/population parameters/coil parameters is *myconstants.py.*
