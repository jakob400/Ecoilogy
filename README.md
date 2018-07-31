# Ecoilogy
---
A genetic algorithm (GA) designed to optimize coil design according to axial field homogeneity.


## Important general definitions:
__Population:__ A group of individuals, where individuals are referring to individual coils.

__Coil:__ A group of wire loops coaxial with the z-axis. Can be also referred to as an "individual" according to the evolutionary analogy. Each individual is conceptually structured around its genetic material, which is to be manipulated by the GA.

__Loop:__ An ideal loop of wire, coaxial with the z-axis.

__Genetic Material:__ The z-positions and currents associated with all the loops in a coil.

__Chromosomes:__ Exactly one half of the genetic material. Each chromosome specifically refers to the z-position and current of a single loop within a coil. Since all coils this program deals with are symmetric, it is sometimes sufficient to deal with only the positive values of the loop positions, along with their corresponding currents.

__Genotype:__ The sum total of the genetic material. The loops on both the positive and negative z-axis, as well as their corresponding currents.


## Important algorithm-specific definitions:
__Parent Fraction:__ The fraction of the total population selected to be parents, according to their superior fitness.

__Lucky Probability:__ The chance that some of the less fit amongst the population will become parents. This has the purpose of maintaining genetic diversity within a population, to help avoid local minima.

__Mutation Probability:__ The chance that a given chromosome within a coil will be mutated. This is currently being treated as 1.

__(z or I) epsilon:__ Once a chromosome has been selected for mutation, this is the upper bound for the range from which perturbations will be chosen to mutate the chromosome.


## How to run the GA:
The program can be run by executing `main.py`:

`python3 main.py`

Once the program has started, it can be closed by pressing `q` and then the **ENTER** key.



Again, once the program has started, the z-epsilon value can also be changed by pressing `z` and the **ENTER** key, and waiting for the prompt:

`What would you like the new value of epsilon to be?`

Note: sometimes the **ENTER** key must be pressed multiple times before this message will be seen. Once it is seen, input the desired value for epsilon, and press the **ENTER** key one final time.


## How to analyze output from the GA:
If the program has been quit successfully using the `q` command, there should be a new folder in the `Output/` directory, along with various output files, as well as a folder of all the chromosomes of the best individual from each generation that experienced a genetic advancement. These are stored as pickled data structures.

Even if the program was quit abruptly or unintentionally, the pickled structures should still be present for analysis.

After a successful quit, main.py will produce images relating to the run and leave them in the appropriate `Output/~` directory.

## Folder Map:
### Output
Contains the output folders for every run, with various output information and graphics.

### Classes
Contains the Population() and Coil() data structures.

### Modules
Contains the functionalities necessary for most algorithm operations. Also contains the algorithm parameters.

#### Genetix.py
Contains functions related to the broader genetic operations. For example, it contains the methods `chrom2geno()` and `chrom_mutate()`, which convert chromosomes to a genotype, and mutates chromosomes, respectively.

#### Magnetix.py
Contains functions specific to magnetic field calculations and other physics required for the algorithm to operate successfully. For example, it contains the methods `field_along_axis()` and `fitness_function()`, which calculate the magnetic field along the axis of a coil, and calculate the fitness of a coil, respectively.

#### Myconstants.py
Contains the operational parameters for the algorithm. For example, it stores variables like the `radius`, `population_number`, and `loop_number`. It also stores the Boolean values of the various mutation methods.

N.B. if a mutation method is set to true, e.g. `PILEUP = True`, then that scheme will be the one implemented in `Coil().mutate()`. For now, the onus is on the user to make sure only one of the the methods is set to `True`, while all others are set to `False`.

#### Writer.py
Contains the functionality to create the proper `Output/` directory for a given run, as well as functions which can be called to write specific files to said directory. This also calls functions from `Analysis.graphical` N.B. There is some code to be executed in the main part of `writer.py`, so as soon as it is imported (in `main.py`), the appropriate directory will be made.


### Analysis
Contains `graphical.py`, whose job it is to create plots to outline and visually demonstrate the key aspects of a given run.

## Different mutation schemes:

### Pileup:

Any chromosomes which have been mutated past their I_max or z_max, will be replaced with their I_max or z_max.


### Reflect

Here, any chromosomes which have been mutated past their I_max or z_max, will be reflected back **before** their I_max or z_max by an equal amount.


### Redraw

Finally, this scheme replaces faulty chromosomes with randomly redrawn chromosomes within the appropriate ranges for position and current.



## Assorted notes:
The only file which should be modified to alter evolutionary performance/population parameters/coil parameters is `myconstants.py.`
