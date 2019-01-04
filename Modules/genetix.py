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
    full_genotype   = [{'z' : -c['z'], 'I' : c['I'], 'r' : c['r']} for c in half_genotype] + half_genotype
    full_genotype   = np.array(full_genotype)

    genotype        = coil_order(full_genotype)

    return genotype

def random_ChromGen(total_loops, loop_z_min, loop_z_max, current_min, current_max, rad_min, rad_max):
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
    ri              = rad_min
    rf              = rad_max

    # Developing chromosomes:
    positions       = np.random.uniform(zi, zf, (chrom_number))
    currents        = np.random.uniform(Ii, If, (chrom_number))
    radii           = np.random.choice([ri, ri], (chrom_number)) # np.random.choice([ri, rf], (chrom_number))
    # radii           = np.random.uniform(ri, rf, (chrom_number))
    chromosomes     = [ {'z' : pos, 'I' : cur, 'r' : rad} for pos,cur,rad in zip(positions, currents, radii) ]

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

def lw_ChromGen(genotype, std_radius):
    """
    Generates exact Lee-Whiting chromosomes according to total current from number of loops allowed and radii of said loops. Radius of loops should be std_radius.

    Input: Number of total loops, radius of standard solenoid.
    Output: Lee-Whiting chromosomes.

    ## FIXME:
    Note: chromosomes should be placed at
    """
    # Relevant assignments:
    b_1     = (0.243186) * std_radius # Distance of inner coils
    b_2     = (0.940733) * std_radius # Distance of outer coils
    total_loops = len(genotype)

    #total_current = sum([x['I'] for x in genotype])
    total_current = total_loops * 1
    half_current  = total_current / 2
    I_1           = half_current / (1 + 2.26044)
    I_2           = half_current - I_1

    chromosomes = [
        {'z' : b_1, 'I' : I_1, 'r' : std_radius},
        {'z' : b_2, 'I' : I_2, 'r' : std_radius}
    ]

    return chromosomes

def lwb_ChromGen(genotype, std_radius):
    """
    Generates approximate (9/4) Lee-Whiting chromosomes according to total current from number of loops allowed and radii of said loops. Places loops at std_radius.

    Input: Number of total loops, radius of standard solenoid.
    Output: Lee-Whiting chromosomes.
    """
    # Relevant assignments:
    b_1     = (0.243186) * std_radius # Distance of inner coils
    b_2     = (0.940733) * std_radius # Distance of outer coils
    total_loops = len(genotype)

    #total_current = sum([x['I'] for x in genotype])
    total_current = total_loops * 1
    half_current  = total_current / 2
    I_1           = half_current / (1 + 2.25)
    I_2           = half_current - I_1

    chromosomes = [
        {'z' : b_1, 'I' : I_1, 'r' : std_radius},
        {'z' : b_2, 'I' : I_2, 'r' : std_radius}
    ]

    return chromosomes
#
# def lw_oldChromGen(total_loops, radius):
#     """
#     Generates (approximate) Lee-Whiting chromosomes according to number of loops allowed and radii of said loops.
#
#     Input: Number of total loops, radius of loops.
#     Output: Lee-Whiting chromosomes.
#     """
#
#     # Relevant assignments:
#     b_1     = (0.243186) * radius # Distance of inner coils
#     b_2     = (0.940733) * radius # Distance of outer coils
#     N       = total_loops
#     N_1     = math.floor( N / (1 + 2.26044) ) # Turns in inner coil
#     N_2     = N - N_1
#
#     # Developing both coils:
#     chromosomes_1 = [{'z' : b_1, 'I' : 1} for _ in range(int(N_1 / 2))]
#     chromosomes_2 = [{'z' : b_2, 'I' : 1} for _ in range(int(N_2 / 2))]
#
#     # Combining coils
#     chromosomes = chromosomes_1
#     chromosomes.extend(copy.deepcopy(chromosomes_2))
#
#     # Ordering chromosomes
#     chromosomes = coil_order(chromosomes)
#
#     return chromosomes



def hh_ChromGen(genotype, std_radius):
    """
    Generates Helmholtz chromosomes according to number of loops allowed and radii of said loops. Loops have radius of std_radius.

    Input: Number of total loops, radius of loops.
    Output: Helmholtz chromosomes.

    """

    # Relevant assignments:
    total_loops     = len(genotype)
    chrom_number    = int(total_loops / 2)
    half_current    = chrom_number

    # Developing chromosomes:
    chromosomes  = [
        {'z' : std_radius / 2, 'I' : half_current, 'r' : std_radius}
    ] # Is putting all the current on 2 wires, which is why you don't need the same number of wires

    # Ordering
    chromosomes  = coil_order(chromosomes)

    return chromosomes


def sol_ChromGen(genotype, loop_z_max, std_radius):
    """
    Generates Solenoid chromosomes according to number of loops allowed and range of said loops. All loops should be placed at std_radius.

    Input: Number of total loops, maximum loop position.
    Output: Solenoid chromosomes.
    """
    ## TODO: Make clearer
    ## TODO: Keep number of loops the same, but alter current per loop if necessary
    ## FIXME: This will be unfair as soon as the current parameter is freed.
    total_loops = len(genotype)

    # Relevant assignments:
    N                  = total_loops
    zi                 = 0
    zf                 = loop_z_max
    loop_interdistance = (zf - zi) / N
    w                  = loop_interdistance

    # Developing chromosomes:
    positions       = np.linspace(w + zi, zf - w, int(N / 2))
    chromosomes     = [{'z' : z, 'I' : 1, 'r' : std_radius} for z in positions]

    # Ordering:
    chromosomes     = coil_order(chromosomes)

    return chromosomes

def gap_ChromGen(genotype, std_radius, length, precision):
    """
    Generates gapped solenoid according to number of loops allowed and range of said loops. All loops should be placed at std_radius.
    """

    total_loops = len(genotype)
    X_m = gap_function(length / std_radius)
    z = 0

    while (z <= 0.5):
        if(gap_function(z / std_radius) < X_m):
            z += precision
        else:
            break
    chrom_number = total_loops / 2
    positions = np.linspace(z, length, chrom_number)
    chromosomes = [{'z' : position, 'I' : 1, 'r' : std_radius} for position in positions]

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




def chrom_mutate(chromosomes, z_epsilon, I_epsilon, r_epsilon):
    """
    Mutate all chromosomes randomly within some range of epsilons.

    Input: Chromosomes (could support genotype), z_epsilon, I_epsilon, r_epsilon
    Output: Mutated positions, mutated currents, mutated radii

    Note: May want to change to not mutate all chromosomes. Or even change to normal distribution.
    """

    positions   = np.array([ d['z'] for d in chromosomes ])
    currents    = np.array([ d['I'] for d in chromosomes ])
    radii       = np.array([ d['r'] for d in chromosomes])

    # m = self.mutation_probability # DON'T NEED THIS FOR NOW
    k_z = random_kGen(z_epsilon, positions.shape) # perturbation amounts for each chromosome position
    k_I = random_kGen(I_epsilon, currents.shape) # perturbation amounts for currents
    k_r = random_kGen(r_epsilon, radii.shape )

    mutated_positions   = (positions * (1 + k_z))
    mutated_currents    = (currents  * (1 + k_I))
    mutated_radii       = (radii     * (1 + k_r))

    return mutated_positions, mutated_currents, mutated_radii


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


def pileupCorrect(mutated_positions, mutated_currents, mutated_radii, loop_z_min, loop_z_max, current_min, current_max, r_min, r_max):
    """
    Correct mutated chromosomes according to pileup method. Chromosomes which have I>I_max or z>z_max are reverted back to I=I_max and z=z_max.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    corrected_positions = genPileupCorrectOperation(mutated_positions, loop_z_min, loop_z_max)
    corrected_currents  = genPileupCorrectOperation(mutated_currents, current_min, current_max)
    corrected_radii     = genPileupCorrectOperation(mutated_radii, r_min, r_max)

    corrected_chromosomes = [ {'z' : pos, 'I' : cur, 'r' : rad} for pos,cur,rad in zip(corrected_positions, corrected_currents, corrected_radii) ]

    return corrected_chromosomes


def reflectCorrect(mutated_positions, mutated_currents, mutated_radii, loop_z_min, loop_z_max, current_min, current_max, r_min, r_max):
    """
    Correct mutated chromosomes according to reflection method. Chromosomes which have I>I_max or z>z_max are reverted back to the same amount below the limits.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    corrected_positions = genReflectCorrectOperation(mutated_positions, loop_z_min, loop_z_max)
    corrected_currents  = genReflectCorrectOperation(mutated_currents, current_min, current_max)
    corrected_radii     = genReflectCorrectOperation(mutated_radii, r_min, r_max)

    corrected_chromosomes   = [ {'z' : pos, 'I' : cur, 'r' : rad} for pos,cur,rad in zip(corrected_positions, corrected_currents, corrected_radii) ]

    return corrected_chromosomes


def redrawCorrect(mutated_positions, mutated_currents, mutated_radii, loop_z_min, loop_z_max, current_min, current_max, r_min, r_max):
    """
    Correct mutated chromosomes according to redraw method. Chromosomes which have I>I_max or z>z_max are redrawn randomly within the appropriate limits.

    Input: Mutated positions, mutated currents, and minimum/maximum values of z and I.
    Output: Corrected chromosomes.
    """

    z_min = loop_z_min
    z_max = loop_z_max
    I_min = current_min
    I_max = current_max
    r_min = r_min
    r_max = r_max

    for i in range(len(mutated_currents)):

        if (mutated_positions[i] > z_max):

            mutated_positions[i] = np.random.uniform(z_min,z_max)

        if (mutated_currents[i]  > I_max):

            mutated_currents[i]  = np.random.uniform(I_min,I_max)

        if (mutated_radii[i] > r_max):

            mutated_radii[i] = np.random.uniform(r_min, r_max)

    corrected_chromosomes = [ {'z' : pos, 'I' : cur, 'r' : rad} for pos,cur,rad in zip(mutated_positions, mutated_currents, mutated_radii) ]

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

def chromRealisticize(chromosomes, mill_precision, wire_width, wall_width, max_stack, r_min):
    """
    Algorithm: Receives chromosome positions. This function has the job of making the chromosomes realistic and millable. This can be summarized by the following criteria:
        1. Reduced precision.
        2. Wire diameter is taken into account.
        3. Wires cannot overlap.
        4. Wires that overlap stack.
        5. If more than two wires are already stacked, third wire is shifted directly beside the stack.
            - If the shifting causes a wire to move past the coil boundaries, then decide how to accommodate. Some options are:
                > Reflect backwards
                > Sub-Algorithm 2:
                    * Begin pileup; place at end of coil.
                    * If too many are stacked, place new wire before last wire
                    * If still on top of two wires, continue bringing back from edge.

                    , begin to bring back from edge. Coil pattern should materialize as flush stacks of two wires coming from end of coil.


    Steps:
        1. Reduce precision (This may cause some stacking)
        2. Create sister dictionary {position: wires_stacked}
        3. Check if stacks of three. If so, push top over by "mill precision" amount.




        2. Check for stacked wires.
        3. Unstack towers of more than 2 wires.
        4.

        NB: radii are not changed yet
    """

    chromosomes  = sorted(chromosomes, key=lambda k: k['z'])

    round_positions = []
    for chromosome in chromosomes: # Rounding positions in chromosomes
        chromosome['z'] = arbitraryRound(chromosome['z'], mill_precision) # Precision now reduced
        round_positions.append(chromosome['z'])


    newB = []


    for i in range(len(chromosomes) - 1):
        pos1 = chromosomes[i]['z']
        rad1 = chromosomes[i]['r']
        pos2 = chromosomes[i+1]['z']
        rad2 = chromosomes[i+1]['r']

        pos2, rad2 = realisticTree(pos1, pos2, rad1, rad2, wire_width, wall_width, max_stack, r_min)
        chromosomes[i+1]['z'] = pos2
        chromosomes[i+1]['r'] = rad2






    # new_chromosomes = []
    # round_positions = []
    #
    #
    #
    #
    # # Now that chromosomes have been rounded:
    # unique_positions        = np.unique(precise_positions) # Getting set of unique values only
    # positions_dict          = {}
    #
    # for position in unique_positions:
    #     positions_dict      = {position: 0} # Filling a dict with zeros, as well as all the positions
    #
    # for position in round_positions:
    #     positions_dict[position] += 1 # Adding a value for each position in this dictionary. Keeping track of stacked positions.
    #
    # # for position in positions_dict:
    # #     if (positions_dict[position] > 2):
    #
    #
    # for i in range(len(chromosomes) - 1):
    #
    #     previous_chromosome = chromosomes[i]
    #     current_chromosome  = chromosomes[i+1]
    #
    #     previous_pos        = previous_chromosome['z']
    #     current_pos         = current_chromosome['z']
    #
    #     if (positions_dict[previous_pos] > 2):
    #         current_pos = previous_pos + wire_width # What happens if there's a loop here?? -> next iteration hopefully should take care of it
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #     if isOverlapping(previous_pos, current_pos, wire_width): # Checks if two wires have any physical overlap.
    #         if (positions_dict[previous_pos] < 2): # value >= 2 is considered stacked (this shouldn't ever be 0 either)
    #             if (pushOver(previous_pos, current_pos) > z_max) # Checks if a forward stack would push over edge.
    #                 pushBack()
    #
    #                 current_chromosome['z'] = pushOver(previous_chromosome['z'],current_pos)
    #         else:
    #             current_chromosome['z'] = previous_chromosome['z']
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # for i in range(len(chromosomes)):
    #     previous_chromosome = chromosome[i]
    #     current_chromosome = chromosomes[i+1]
    #
    #     previous_chromosome['z'] = arbitraryRound(previous_chromosome['z'],div_width)
    #     if (isOverlapping(previous_chromosome['z'],current_chromosome['z'])):
    #         correctOverlap(previous_chromosome,current_chromosome)
    #
    #
    #
    #
    #     # chromosomes[j]['z'] = arbitraryRound(chromosomes[])
    #
    #
    # for chromosome in chromosomes:
    #     chromosome['z'] = arbitraryRound(chromosome['z'], div_width)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # for chromosome in chromosomes:
    #     chromosome['z'] = np.round(a=chromosome['z'], decimals=div_width)
    #     other_chromosomes   = list(chromosomes)
    #     other_chromosomes.remove(chromosome)
    #
    #
    #     new_chromosome      = millingGuide(chromosome, other_chromosomes)
    #
    #
    #     old_position        = chromosome['z']
    #
    #
    #     new_chromosome      = {'z' : arbitraryRound(old_position, mill_precision),
    #                            'r' : chromosome['r'],
    #                            'I' : chromosome['I']}
    #     new_chromosomes = new_chromosomes.append(new_chromosome)
    #
    #
    #
    #
    # realistic_chromosomes = copy.deepcopy(chromosomes)

    return chromosomes


def realisticTree(pos1, pos2, rad1, rad2, wire_width, wall_width, max_stack, r_min):
    """
    Decides what to do with wire 2 (pos2) based on its distance from wire 1 (pos1).

    Input: pos1 [scalar], pos2 [scalar], wire_width [scalar], wall_width [scalar]
    Output: pos2 [scalar] (adjusted position of wire 2)
    """
    stacked_at_pos1 = int((rad1 - r_min) / wire_width) # This is the number of wires stacked at pos1

    if (pos2 - pos1 < wall_width + wire_width):
        if(pos2 - pos1 < wire_width):
            if(pos2 - pos1 < wire_width/2):
                if(stacked_at_pos1 > max_stack):
                    pos2 = pos1 + wire_width
                else:
                    pos2 = pos1
                    rad2 = rad1 + wire_width
            else:
                pos2 = pos1 + wire_width
        else:
            pos2 = pos1 + wall_width + wire_width
    return pos2, rad2

def millingGuide(chromosome, other_chromosomes):
    # FIXME: What to do if chromosome is pushed past boundary of Coil limits
    # TODO: Make sure that any successive calculations don't infringe on prior calculations


    # chromosome['z']     = arbitraryRound(chromosome['z'], other_chromosomes, mill_precision)
    # chromosome['z']     = wallDecision(chromosome['z'], other_chromosomes, wall_width)


    chromosome['z']     = unStack(chromosome['z'], other_chromosomes, wire_width)

    return chromosome

def wallDecision(position, other_chromosomes, wall_width):
    for other_chromosome in other_chromosomes:
        other_position  = other_chromosome['z']
        difference      = position - other_position

        # If wires are less than wall width apart:

        # Algorithm:
        # If wire edges are less than wall width apart, then decide if they
        # should go beside each other, or apart by a wall width




def unStack(position, other_chromosomes, wire_width):

    for other_chromosome in other_chromosomes:
        other_position  = other_chromosome['z']
        difference      = position - other_position

        # If wire centres are less than (1/2)(wall_width + wire_width) apart:
        if (abs(difference) < (wire_width)):
            # If current wire is BELOW other wire:
            if (difference < 0):
                newPosition = other_position - wire_width
            # If current wire is ABOVE other wire:
            else:
                newPosition = other_position + wire_width

    return newPosition

def arbitraryRound(value, roundPrecision):
    """
    Rounds input value to integer multiple of arbitrary amount.

    Input: Value to be rounded, amount to round to. (must be below 0.5?)
    Output: Rounded value.
    """
    remainder   = value % roundPrecision
    complement  = roundPrecision - remainder
    if (remainder >= (roundPrecision / 2) ):
        newValue = value + complement
    else:
        newValue = value - remainder

    return newValue
