# Ecoilogy

A genetic algorithm (GA) designed to optimize coil design according to axial field homogeneity.


## Important general definitions:
--------------------------------
__Population:__ A group of individuals, where individuals are referring to individual coils.

__Coil:__ A group of wire loops coaxial with the z-axis. Can be also referred to as an "individual" according to the evolutionary analogy. Each individual is conceptually structured around its genetic material, which is to be manipulated by the GA.

__Loop:__ An ideal loop of wire, coaxial with the z-axis.

__Genetic Material:__ The z-positions and currents associated with all the loops in a coil.

__Chromosomes:__ Exactly one half of the genetic material. Each chromosome specifically refers to the z-position and current of a single loop within a coil. Since all coils this program deals with are symmetric, it is sometimes sufficient to deal with only the positive values of the loop positions, along with their corresponding currents.

__Genotype:__ The sum total of the genetic material. The loops on both the positive and negative z-axis, as well as their corresponding currents.


## Important algorithm-specific definitions:
--------------------------------
__Parent Fraction:__ The fraction of the total population selected to be parents, according to their superior fitness.

__Lucky Probability:__ The chance that some of the less fit amongst the population will become parents. This has the purpose of maintaining genetic diversity within a population, to help avoid local minima.

__Mutation Probability:__ The chance that a given chromosome within a coil will be mutated. This is currently being treated as 1.

__(z or I) epsilon:__ Once a chromosome has been selected for mutation, this is the upper bound for the range from which perturbations will be chosen to mutate the chromosome.


## How to run the GA:
--------------------------------
The program can be run by executing *main.py*:

`python3 main.py`

Once the program has started, it can be closed by pressing `q` and then the **ENTER** key.



Again, once the program has started, the z-epsilon value can also be changed by pressing `z` and the **ENTER** key, and waiting for the prompt:

`What would you like the new value of epsilon to be?`

Note: sometimes the **ENTER** key must be pressed multiple times before this message will be seen. Once it is seen, input the desired value for epsilon, and press the **ENTER** key one final time.


## How to analyze output from the GA:
--------------------------------
If the program has been quit successfully using the `q` command, there should be a new folder in the *Output/* directory, along with various output files, as well as a folder of all the chromosomes of the best individual from each generation that experienced a genetic advancement. These are stored as pickled data structures.

Even if the program was quit abruptly or unintentionally, the pickled structures should still be present for analysis.


Within the main directory, the two relevant extraction scripts are *waterfall_plotter.py* and *fitness_check.py*. Here's a quick summary of their roles:

#### waterfall_plotter.py:

This extracts all the of the pickled chromosomes, and then plots their positions along the z-axis, descending vertically according to generation number.

#### fitness_check.py:

This allows the user to input the range and number of of analysis points over which they wish to calculate homogeneity for the **best coil in the last generation** . This also produces and saves plots which depict the field along the axis as well.

### How to run these:
At the top of each of these scripts, there is a variable declaration for the string variable `folder`. Simply change the stored string to the output folder of interest:

`folder = 'Output/Friday27.14:33:33@10/'`


## Different mutation schemes:
--------------------------------

### Pileup:

Any chromosomes which have been mutated past their I_max or z_max, will be replaced with their I_max or z_max.


### Reflect

Here, any chromosomes which have been mutated past their I_max or z_max, will be reflected back **before** their I_max or z_max by an equal amount.


### Redraw

Finally, this scheme replaces faulty chromosomes with randomly redrawn chromosomes within the appropriate ranges for position and current.




The only file which should be modified to alter evolutionary performance/population parameters/coil parameters is *myconstants.py.*
