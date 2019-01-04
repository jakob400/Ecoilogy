import random
import numpy as np

import Modules.myconstants as myconst
import Modules.magnetix as mag
import Modules.genetix as gen

#TODO: Consider changing zlist to fitness_zlist, or field_zlist, for clarity

class Coil:
    """
    Coil object. Contains coil's genotype and fitness.

    Constructed so that the chromosomes define the behaviour of all update
    functions.

    ##FIXME: All perfect coils should have loops at std_radius. Otherwise stack at r_min.
    """

    ### Instance Attributes:
    ## Evolutionary traits:
    genotype    = [] # All values
    chromosomes = [] # Just positive values
    field       = []
    ppm         = []
    fitness     = None


    ### Class Attributes:
    ## Mutation Scheme
    MutationScheme = myconst.MutationScheme

    ## Range of coil:
    z_min   = myconst.z_min
    z_max   = myconst.z_max

    ## Range of current:
    I_min   = myconst.I_min
    I_max   = myconst.I_max

    ## Range of radii:
    std_radius  = myconst.r_0
    r_min       = myconst.r_min
    r_max       = myconst.r_max

    ## Realism Parameters:
    div_width       = myconst.div_width
    gap_precision   = myconst.gap_precision
    mill_precision  = myconst.mill_precision # The
    wire_width      = myconst.wire_width
    wall_width      = myconst.wall_width

    ## Range of Fitness Calculation:
    calc_z_min  = myconst.calc_z_min
    calc_z_max  = myconst.calc_z_max
    calc_points = myconst.calc_points
    zlist       = np.linspace(calc_z_min,calc_z_max,calc_points) # Calculation points
    field_points= zlist

    walk_limit  = myconst.walk_limit
    div_width   = myconst.div_width

    ## Initial values
    loop_number     = myconst.loop_number
    radius          = myconst.r_0
    epsilon         = myconst.epsilon
    I_epsilon       = myconst.I_epsilon
    r_epsilon       = myconst.r_epsilon
    # wire_width      = myconst.wire_width
    gap_precision   = myconst.gap_precision

    chromosomes     = gen.random_ChromGen(loop_number, z_min, z_max, I_min, I_max, r_min, r_max)
    genotype        = gen.chrom2geno(chromosomes)


    # gen.lw_ChromGen(genotype, radius)
    # gen.sol_ChromGen(genotype, loop_z_max, radius)
    # gen.lwb_ChromGen(genoptype, radius)
    # gen.hh_ChromGen(genotype, radius)
    # gen.gap_ChromGen(genotype, precision, radius)

    ## Standards:
    # Building Solenoid:
    sol_chromosomes = np.array(gen.sol_ChromGen(genotype, z_max, std_radius))
    sol_genotype    = np.array(gen.chrom2geno(sol_chromosomes))
    sol_homogeneity = mag.fitness_function(sol_genotype, field_points)

    # Building Lee-Whiting:
    lw_chromosomes = np.array(gen.lw_ChromGen(genotype, std_radius))
    lw_genotype    = np.array(gen.chrom2geno(lw_chromosomes))
    lw_homogeneity = mag.fitness_function(lw_genotype, field_points)

    # Building 9/4 Lee-Whiting:
    lwb_chromosomes = np.array(gen.lwb_ChromGen(genotype, std_radius))
    lwb_genotype    = np.array(gen.chrom2geno(lwb_chromosomes))
    lwb_homogeneity = mag.fitness_function(lwb_genotype, field_points)

    # Building Helmholtz:
    hh_chromosomes = np.array(gen.hh_ChromGen(genotype, std_radius))
    hh_genotype    = np.array(gen.chrom2geno(hh_chromosomes))
    hh_homogeneity = mag.fitness_function(hh_genotype, field_points)

    # Building Gapped Solenoid:
    gap_chromosomes = np.array(gen.gap_ChromGen(genotype, std_radius, z_max, mill_precision))
    gap_genotype    = np.array(gen.chrom2geno(gap_chromosomes))
    gap_homogeneity = mag.fitness_function(gap_genotype, field_points)



    def __init__(self):
        """Coil initialization. Creates random genotype and sets fitness to 0."""

        self.chromosomes_init()
        self.genotype_update()
        self.fitness_update()
        self.field_update()


    def manual_chromosomes_update(self, chromosomes):
        """Manually sets the chromosomes for an individual."""

        self.chromosomes = chromosomes
        self.genotype_update()
        self.fitness_update()
        self.field_update()


    def chromosomes_init(self):
        """
        Genotype initialization. Randomly chooses loop positions along z-axis.
        Positions act as individual chromosomes.

        ## NOTE: Currently note actually generating loops at different radii. The range is [r_min, r_min]
        """
        self.chromosomes = gen.random_ChromGen(Coil.loop_number, Coil.z_min, Coil.z_max, Coil.I_min, Coil.I_max, Coil.r_min, Coil.r_max)


    def genotype_update(self):
        """
        Takes chromosomes and converts to genotype.
        """
        #self.chromosomes    = gen.chromRealisticize(self.chromosomes, Coil.wire_width, self.mill_precision)
        self.genotype       = gen.chrom2geno(self.chromosomes)


    def fitness_update(self):
        """Updates fitness of self"""
        self.fitness = mag.fitness_function(self.genotype, Coil.zlist)


    def field_update(self):
        """Updates the fields along the axis."""
        args = [self.genotype, Coil.zlist]

        self.field  = mag.field_along_axis(*args)
        self.ppm    = mag.ppm_field(*args)


    def mutate(self):
        """
        Mutates chromosomes randomly with probability m.

        Note: Currently mutates ALL chromosomes, maybe change later.
        FIXME: Mutation probability must be handled externally.
        """
        mutated_positions, mutated_currents, mutated_radii  = gen.chrom_mutate(self.chromosomes, Coil.epsilon, Coil.I_epsilon, Coil.r_epsilon)

        args = [mutated_positions, mutated_currents, mutated_radii, Coil.z_min, Coil.z_max, Coil.I_min, Coil.I_max, Coil.r_min, Coil.r_max]

        if (Coil.MutationScheme == 'PILEUP'):
            mutated_chromosomes = gen.pileupCorrect(*args)

        elif(Coil.MutationScheme == 'REFLECTION'):
            mutated_chromosomes = gen.reflectCorrect(*args)

        elif(Coil.MutationScheme == 'REDRAW'):
            mutated_chromosomes = gen.redrawCorrect(*args)

        elif(Coil.MutationScheme == 'SPREADOUT'):
            pass

        else:
            print('INVALID MUTATION SCHEME')
            exit()

        # Assigning changes to instance:
        self.chromosomes = gen.coil_order(mutated_chromosomes)
        self.genotype_update()
