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
    # Relevant assignments:
    b_1     = (0.243186) * radius # Distance of inner coils
    b_2     = (0.940733) * radius # Distance of outer coils

    #total_current = sum([x['I'] for x in genotype])
    total_current = total_loops * 1
    half_current  = total_current / 2
    I_1           = half_current / (1 + 2.26044)
    I_2           = half_current - I_1

    chromosomes = [
        {'z' : b_1, 'I' : I_1},
        {'z' : b_2, 'I' : I_2}
    ]

    return chromosomes

def lw_oldChromGen(total_loops, radius):
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
    ## TODO: Make clearer

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

def gap_ChromGen(radius, length, total_loops, precision):

    X_m = gap_function(length / radius)
    z = 0

    while (z <= 0.5):
        if(gap_function(z / radius) < X_m):
            z += precision
        else:
            break
    chrom_number = total_loops / 2
    positions = np.linspace(z, length, chrom_number)
    chromosomes = [{'z': position, 'I':1} for position in positions]

    return chromosomes

def gap_function(X):
    return X * (1 + X ** 2) ** (-5/2)


def coil_order(genetic_material):
    """
    Orders genetic material according to positions of loops.

    Input: Chromosomes or Genotype.
    Output: Ordered genetic material according to fitness. (largest -> smallest)
    """

    ordered_genetics = sorted(genetic_material, key=lambda k: k['z'])
    ordered_genetics = np.array(ordered_genetics)

    return ordered_genetics



# def population_order(pop):
#     return ordered_pop




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


def genPileupCorrectOperation(mutated_values, min_val, max_val):
    """
    Generalized operation to correct errors due to Pileup mutation method.

    Input: Mutated values, minimum expected value, maximum expected value.
    Output: Corrected values.
    """

    values    = np.array(mutated_values)

    ## Converting values to Boolean equivalents:
    Bool_bad_above = (values > max_val).astype(int) # All values above threshold
    Bool_bad_below = (values < min_val).astype(int) # All values below threshold
    Bool_good      = (Bool_bad_above == Bool_bad_below).astype(int) # All values at or within thresholds

    ## Using Boolean arrays to isolate bad values and replace with thresholds
    corrected_above   = Bool_bad_above * max_val # Converting bad above to upper threshold
    corrected_below   = Bool_bad_below * min_val # Converting bad below to lower threshold
    good_initial      = Bool_good * values # Retaining good values

    ## Recombining
    corrected_values = corrected_above + corrected_below + good_initial # Vector addition

    return corrected_values


def genReflectCorrectOperation(mutated_values, min_val, max_val):
    """
    Generalized operation to correct errors due to Reflect mutation method.

    Input: Mutated values, minimum expected value, maximum expected value.
    Output: Corrected values.
    """

    values    = np.array(mutated_values)

    ## Converting values to Boolean equivalents:
    Bool_bad_above = (values > max_val).astype(int)
    Bool_bad_below = (values < min_val).astype(int)
    Bool_good      = (Bool_bad_above == Bool_bad_below).astype(int)

    ## Getting back arrays with only the relevant parts as nonzero:
    bad_above     = Bool_bad_above * values # All values above threshold
    bad_below     = Bool_bad_below * values # All values below threshold
    good_initial  = Bool_good      * values # All values at or within thresholds

    ## Formula: 2 * z_max - z_mut = z_cor
    corrected_above = 2 * max_val * Bool_bad_above - bad_above
    corrected_below = 2 * min_val * Bool_bad_below - bad_below

    ## Combining to correct
    corrected_values = corrected_above + corrected_below + good_initial

    return corrected_values


def pileupCorrect(mutated_positions, mutated_currents, loop_z_min, loop_z_max, current_min, current_max):
    """
    Correct mutated chromosomes according to pileup method. Chromosomes which have I>I_max or z>z_max are reverted back to I=I_max and z=z_max.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    corrected_positions = genPileupCorrectOperation(mutated_positions, loop_z_min, loop_z_max)
    corrected_currents  = genPileupCorrectOperation(mutated_currents, current_min, current_max)

    corrected_chromosomes = [ {'z' : pos, 'I' : cur} for pos,cur in zip(corrected_positions, corrected_currents) ]

    return corrected_chromosomes


def reflectCorrect(mutated_positions, mutated_currents, loop_z_min, loop_z_max, current_min, current_max):
    """
    Correct mutated chromosomes according to reflection method. Chromosomes which have I>I_max or z>z_max are reverted back to the same amount below the limits.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    corrected_positions = genReflectCorrectOperation(mutated_positions, loop_z_min, loop_z_max)
    corrected_currents  = genReflectCorrectOperation(mutated_currents, current_min, current_max)

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

def last_difference_calc(best_fitness_list):
    """
    Calculates how many generations have passed since the last change.

    Input: List of best fitnesses from all generations so far.
    Output: Number of generations since last change.
    """
    #TODO: Ask dave if there is a better way to do this
    last_difference = 0

    # TODO: FIXME
    # for i in range(1, len(best_fitness_list) + 1):
    for i in range(1, len(best_fitness_list)):
        if (best_fitness_list[-i] == best_fitness_list[-i-1]):
            last_difference += 1
        else:
            break

    return last_difference


def epsilonCalc(last_difference, generation):
    """
    Calculates what epsilon should be based on how long ago the last evolutionary advancement was. Essentially a metric of health of population. Amount is (roughly) inversely proportional to population stagnation.

    Input: Last evolutionary advancement (int)
    Output: New Epsilon (float)
    """

    x       = last_difference
    y       = generation
    power   = 1 / 10
    scale   = 0.5
    factor  = 10
    R       = 5 * x + .05 * y  # last_difference should make more of an impact than generation

    newEpsilon  = math.exp( math.log(scale) - power * (R + math.log(factor + math.exp(-R)))  )

    return newEpsilon

def chromRealisticize(chromosomes, wire_width):
    for chromosome in chromosomes:
        chromosome['z'] = np.round(a=chromosome['z'], decimals=wire_width)

    realistic_chromosomes = copy.deepcopy(chromosomes)

    return realistic_chromosomes
