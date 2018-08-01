import numpy as np
import math
import copy
import random

def chrom2geno(chromosomes):
    """
    Converts chromosomes to genotype.

    Input: Array of chromosomes.
    Output: Array of genotype.
    """

    half_genotype   = list(chromosomes)
    full_genotype   = [{'I' : c['I'], 'z' : -c['z']} for c in half_genotype] + half_genotype
    full_genotype   = np.array(full_genotype)

    genotype        = coil_order(full_genotype)

    return genotype

def random_ChromGen(total_loops, loop_z_min, loop_z_max, current_min, current_max):
    """
    Generates randomly placed chromosomes. Randomly chooses loop positions along z-axis and current values.
    Positions act as individual chromosomes.
    """

    # Relevant assignments:
    chrom_number    = int(total_loops / 2)
    zi              = loop_z_min
    zf              = loop_z_max
    Ii              = current_min
    If              = current_max

    # Developing chromosomes:
    positions       = np.random.uniform(zi, zf, (chrom_number))
    currents        = np.random.uniform(Ii, If, (chrom_number))
    chromosomes     = [ {'z' : pos, 'I' : cur} for pos,cur in zip(positions, currents) ]

    # Ordering:
    chromosomes  = sorted(chromosomes, key=lambda k: k['z']) # Sorting according to value of 'z' keys in dicts within list

    return chromosomes

def random_kGen(epsilon, shape):
    """
    Generates vector of randomly chosen values between -epsilon and +epsilon with defined shape.

    Input: Mutation amount (epsilon), shape of vector (shape)
    Ouput: Mutation vector 'k'.
    """

    #k = np.random.uniform(-epsilon, epsilon, shape)
    k = np.random.normal(0, epsilon, shape)

    return k

def lw_ChromGen(total_loops, radius):
    """
    Generates (approximate) Lee-Whiting chromosomes according to number of loops allowed and radii of said loops.

    Input: Number of total loops, radius of loops.
    Output: Lee-Whiting chromosomes.
    """

    # Relevant assignments:
    b_1     = (0.243186) * radius # Distance of inner coils
    b_2     = (0.940733) * radius # Distance of outer coils
    N       = total_loops
    N_1     = math.floor( N / (1 + 2.26044) ) # Turns in inner coil
    N_2     = N - N_1

    # Developing both coils:
    chromosomes_1 = [{'z' : b_1, 'I' : 1} for _ in range(int(N_1 / 2))]
    chromosomes_2 = [{'z' : b_2, 'I' : 1} for _ in range(int(N_2 / 2))]

    # Combining coils
    chromosomes = chromosomes_1
    chromosomes.extend(copy.deepcopy(chromosomes_2))

    # Ordering chromosomes
    chromosomes = coil_order(chromosomes)

    return chromosomes


def hh_ChromGen(total_loops, radius):
    """
    Generates Helmholtz chromosomes according to number of loops allowed and radii of said loops.

    Input: Number of total loops, radius of loops.
    Output: Helmholtz chromosomes.
    """

    # Relevant assignments:
    chrom_number = int(total_loops / 2)

    # Developing chromosomes:
    chromosomes  = [{'z' : float(radius / 2), 'I' : 1} for _ in range(chrom_number)]

    # Ordering
    chromosomes  = coil_order(chromosomes)

    return chromosomes


def sol_ChromGen(total_loops, loop_z_max):
    """
    Generates Solenoid chromosomes according to number of loops allowed and range of said loops.

    Input: Number of total loops, maximum loop position.
    Output: Solenoid chromosomes.
    """

    # Relevant assignments:
    N                  = total_loops
    zi                 = 0
    zf                 = loop_z_max
    loop_interdistance = (zf - zi) / N
    w                  = loop_interdistance

    # Developing chromosomes:
    positions       = np.linspace(w + zi, zf - w, int(N / 2))
    chromosomes     = [{'z' : z, 'I' : 1} for z in positions]

    # Ordering:
    chromosomes     = coil_order(chromosomes)

    return chromosomes


def coil_order(genetic_material):
    """
    Orders genetic material according to positions of loops.

    Input: Chromosomes or Genotype.
    Output: Ordered genetic material according to fitness. (largest -> smallest)
    """

    ordered_genetics = sorted(genetic_material, key=lambda k: k['z'])
    ordered_genetics = np.array(ordered_genetics)

    return ordered_genetics



def population_order(pop):
    return ordered_pop




def chrom_mutate(chromosomes, z_epsilon, I_epsilon):
    """
    Mutate all chromosomes randomly within some range of epsilons.

    Input: Chromosomes (could support genotype), z_epsilon, I_epsilon
    Output: Mutated positions, mutated currents

    Note: May want to change to not mutate all chromosomes. Or even change to normal distribution.
    """

    positions = np.array([ d['z'] for d in chromosomes ])
    currents  = np.array([ d['I'] for d in chromosomes ])

    # m = self.mutation_probability # DON'T NEED THIS FOR NOW
    k_z = random_kGen(z_epsilon, positions.shape) # perturbation amounts for each chromosome position
    k_I = random_kGen(0, currents.shape) # perturbation amounts for currents

    mutated_positions = (positions * (1 + k_z))
    mutated_currents  = (currents  * (1 + k_I))

    return mutated_positions, mutated_currents


def pileupCorrect(mutated_positions, mutated_currents, loop_z_min, loop_z_max, current_min, current_max):
    """
    Correct mutated chromosomes according to pileup method. Chromosomes which have I>I_max or z>z_max are reverted back to I=I_max and z=z_max.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    currents    = np.array(mutated_currents)
    positions   = np.array(mutated_positions)

    z_min = loop_z_min
    z_max = loop_z_max
    I_min = current_min
    I_max = current_max

    ## Converting values to Boolean equivalents:
    Bool_bad_above_positions = (positions > z_max).astype(int) # All values above threshold
    Bool_bad_below_positions = (positions < z_min).astype(int) # All values below threshold
    Bool_good_positions      = (Bool_bad_above_positions == Bool_bad_below_positions).astype(int) # All values at or within thresholds

    Bool_bad_above_currents  = (currents > I_max).astype(int)
    Bool_bad_below_currents  = (currents < I_min).astype(int)
    Bool_good_currents       = (Bool_bad_above_currents == Bool_bad_below_currents).astype(int)

    ## Using Boolean arrays to isolate bad values and replace with thresholds
    corrected_above_positions   = Bool_bad_above_positions * z_max # Converting bad above to upper threshold
    corrected_below_positions   = Bool_bad_below_positions * z_min # Converting bad below to lower threshold
    good_initial_positions      = Bool_good_positions * positions # Retaining good values

    corrected_above_currents   = Bool_bad_above_currents * I_max
    corrected_below_currents   = Bool_bad_below_currents * I_min
    good_initial_currents      = Bool_good_currents * currents

    ## Recombining
    corrected_positions = corrected_above_positions + corrected_below_positions + good_initial_positions # Combining to correct
    corrected_currents  = corrected_above_currents  + corrected_below_currents  + good_initial_currents

    corrected_chromosomes = [ {'z' : pos, 'I' : cur} for pos,cur in zip(corrected_positions, corrected_currents) ]

    return corrected_chromosomes


def reflectCorrect(mutated_positions, mutated_currents, loop_z_min, loop_z_max, current_min, current_max):
    """
    Correct mutated chromosomes according to reflection method. Chromosomes which have I>I_max or z>z_max are reverted back to the same amount below the limits.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    currents    = np.array(mutated_currents)
    positions   = np.array(mutated_positions)

    z_min = loop_z_min
    z_max = loop_z_max
    I_min = current_min
    I_max = current_max

    ## Converting values to Boolean equivalents:
    Bool_bad_above_positions = (positions > z_max).astype(int)
    Bool_bad_below_positions = (positions < z_min).astype(int)
    Bool_good_positions      = (Bool_bad_above_positions == Bool_bad_below_positions).astype(int)

    Bool_bad_above_currents = (currents > I_max).astype(int)
    Bool_bad_below_currents = (currents < I_min).astype(int)
    Bool_good_currents      = (Bool_bad_above_currents == Bool_bad_below_currents).astype(int)

    ## Getting back arrays with only the relevant parts as nonzero:
    bad_above_positions     = Bool_bad_above_positions * positions # All values above threshold
    bad_below_positions     = Bool_bad_below_positions * positions # All values below threshold
    good_initial_positions  = Bool_good_positions      * positions # All values at or within thresholds

    bad_above_currents      = Bool_bad_above_currents * currents
    bad_below_currents      = Bool_bad_below_currents * currents
    good_initial_currents   = Bool_good_currents      * currents

    ## Formula: 2 * z_max - z_mut = z_cor
    corrected_above_positions = 2 * z_max * Bool_bad_above_positions - bad_above_positions
    corrected_below_positions = 2 * z_min * Bool_bad_below_positions - bad_below_positions

    corrected_above_currents = 2 * z_max * Bool_bad_above_currents - bad_above_currents
    corrected_below_currents = 2 * z_min * Bool_bad_below_currents - bad_below_currents

    ## Combining to correct
    corrected_positions = corrected_above_positions + corrected_below_positions + good_initial_positions # Combining to correct
    corrected_currents  = corrected_above_currents  + corrected_below_currents  + good_initial_currents

    corrected_chromosomes   = [ {'z' : pos, 'I' : cur} for pos,cur in zip(corrected_positions, corrected_currents) ]

    return corrected_chromosomes


def redrawCorrect(mutated_positions, mutated_currents, loop_z_min, loop_z_max, current_min, current_max):
    """
    Correct mutated chromosomes according to redraw method. Chromosomes which have I>I_max or z>z_max are redrawn randomly within the appropriate limits.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    z_min = loop_z_min
    z_max = loop_z_max
    I_min = current_min
    I_max = current_max

    for i in range(len(mutated_currents)):

        if (mutated_positions[i] > z_max):

            mutated_positions[i] = np.random.uniform(z_min,z_max)

        if (mutated_currents[i]  > I_max):

            mutated_currents[i]  = np.random.uniform(I_min,I_max)

    corrected_chromosomes = [ {'z' : pos, 'I' : cur} for pos,cur in zip(mutated_positions, mutated_currents) ]

    return corrected_chromosomes

def evolution_cycle(pop):
    """
    Performs cycle operation on population to advance generation.

    Input: Population instance.
    Output: Population instance.
    """

    pop.individuals = pop.order(pop.individuals)
    pop.parents_update()
    pop.children_update()
    pop.mutate()
    pop.population_update()
    pop.best_fitness_append()

    return pop

def last_difference_calc(best_fitness_list):
    """
    Calculates how many generations have passed since the last change.

    Input: List of best fitnesses from all generations so far.
    Output: Number of generations since last change.
    """
    #TODO: Ask dave if there is a better way to do this
    last_difference = 0

    for i in range(1, len(best_fitness_list) + 1):
        if (best_fitness_list[-i] == best_fitness_list[-i-1]):
            last_difference += 1
        else:
            break

    return last_difference


def epsilonCalc(last_difference, generation):
    """
    Calculates what epsilon should be based on how long ago the last evolutionary advancement was.

    Input: Last evolutionary advancement (int)
    Output: New Epsilon (float)
    """
    x       = last_difference
    y       = generation
    power   = 1 / 10
    scale   = 0.5
    factor  = 10
    R       = x + 0.1 * y  # last_difference should make more of an impact than generation

    newEpsilon  = math.exp( math.log(scale) - power * (R + math.exp(-R)) )

    # exponent    = math.exp(5 * (x + 0.1 * y))
    # denominator = math.pow(1 + exponent, power)
    # numerator   = 0.5
    #
    # newEpsilon = numerator / denominator

    return newEpsilon
