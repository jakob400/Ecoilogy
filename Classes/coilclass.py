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

    ## Range of Fitness Calculation:
    calc_z_min  = myconst.calc_z_min
    calc_z_max  = myconst.calc_z_max
    calc_points = myconst.calc_points
    zlist       = np.linspace(calc_z_min,calc_z_max,calc_points) # Calculation points

    ## Initial values
    loop_number     = myconst.loop_number
    radius          = myconst.radius
    epsilon         = myconst.epsilon
    I_epsilon       = myconst.I_epsilon

    ## Standards:
    sol_genotype    = []
    sol_chromosomes = []
    sol_homogeneity = 0

    hh_genotype     = []
    hh_chromosomes  = []
    hh_homogeneity  = 0

    lw_genotype     = []
    lw_chromosomes  = []
    lw_homogeneity  = 0


    def __init__(self):
        """Coil initialization. Creates random genotype and sets fitness to 0."""

        self.chromosomes_init()
        self.genotype_update()
        self.fitness_update()
        self.field_update()

        self.hh_init()
        self.lw_init()
        self.sol_init()



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
        """

        # Importing class variables:
        N       = Coil.loop_number
        z_min   = Coil.z_min
        z_max   = Coil.z_max
        I_min   = Coil.I_min
        I_max   = Coil.I_max

        # Generating chromosomes:
        chromosomes = gen.random_ChromGen(N, z_min, z_max, I_min, I_max)

        # Class assignments:
        self.chromosomes = chromosomes


    def genotype_update(self):
        """
        Takes chromosomes and converts to genotype.
        """

        # Importing class variable:
        chromosomes     = self.chromosomes

        # Converting to genotype:
        genotype        = gen.chrom2geno(chromosomes)

        # Instance assignment:
        self.genotype = genotype


    def fitness_update(self):
        """Updates fitness of self"""

        # Importing class variables
        zlist    = Coil.zlist
        a        = Coil.radius

        # Importing instance variables
        genotype = self.genotype

        # Calculating fitness:
        self.fitness = mag.fitness_function(genotype, zlist, a)


    def field_update(self):
        """Updates the fields along the axis."""

        # Importing class variables
        zlist    = Coil.zlist
        a        = Coil.radius

        # Importing instance variables
        genotype = self.genotype

        # Calculating and assigning magnetics (instance):
        self.field  = mag.field_along_axis(genotype, zlist, a)
        self.ppm    = mag.ppm_field(genotype, zlist, a)


    def mutate(self):
        """
        Mutates chromosomes randomly with probability m.

        Note: Currently mutates ALL chromosomes, maybe change later.
        FIXME: Mutation probability must be handled externally.
        """

        # Importing class variables
        z_min       = Coil.z_min
        z_max       = Coil.z_max
        I_min       = Coil.I_min
        I_max       = Coil.I_max
        epsilon     = Coil.epsilon
        I_epsilon   = Coil.I_epsilon

        # Importing instance variables:
        chromosomes = self.chromosomes

        mutated_positions, mutated_currents  = gen.chrom_mutate(chromosomes, epsilon, I_epsilon)

        if (Coil.MutationScheme == 'PILEUP'):
            mutated_chromosomes = gen.pileupCorrect(mutated_positions, mutated_currents, z_min, z_max, I_min, I_max)

        elif(Coil.MutationScheme == 'REFLECTION'):
            mutated_chromosomes = gen.reflectCorrect(mutated_positions, mutated_currents, z_min, z_max, I_min, I_max)

        elif(Coil.MutationScheme == 'REDRAW'):
            mutated_chromosomes = gen.redrawCorrect(mutated_positions, mutated_currents, z_min, z_max, I_min, I_max)

        elif(Coil.MutationScheme == 'SPREADOUT'):
            pass

        else:
            print('INVALID MUTATION SCHEME')
            exit()

        # Assigning changes to instance:
        self.chromosomes = gen.coil_order(mutated_chromosomes)
        self.genotype_update()


    def hh_init(self):
        """
        Calculates field due to Helmholtz coil with the same configuration.
        """

        # Importing class variables:
        a               = Coil.radius
        N               = Coil.loop_number # Total numer of loops available
        field_points    = Coil.zlist

        # Building genetics:
        chromosomes = gen.hh_ChromGen(N, a)
        genotype    = gen.chrom2geno(chromosomes)

        # Class assignments:
        Coil.hh_chromosomes = np.array(chromosomes)
        Coil.hh_genotype    = np.array(genotype)
        Coil.hh_homogeneity = mag.fitness_function(genotype, field_points, a)


    def sol_init(self):
        ## TODO: finish adding currents to chromosomes
        """
        Calculates field due to solenoid with the same configuration.
        """

        # Importing class variables:
        loop_z_max      = Coil.z_max
        N               = Coil.loop_number # Total numer of loops available
        field_points    = Coil.zlist
        a               = Coil.radius

        # Building genetics:
        chromosomes = gen.sol_ChromGen(N, loop_z_max)
        genotype    = gen.chrom2geno(chromosomes)

        # Class assignments:
        Coil.sol_chromosomes = np.array(chromosomes)
        Coil.sol_genotype    = np.array(genotype)
        Coil.sol_homogeneity = mag.fitness_function(genotype, field_points, a)


    def lw_init(self):
        """
        Builds Lee-Whiting genetics and calculates Lee-Whiting fitness.
        """

        # Importing class variables:
        a               = Coil.radius
        N               = Coil.loop_number # Total numer of loops available
        field_points    = Coil.zlist

        # Building genetics:
        chromosomes = gen.lw_ChromGen(N, a)
        genotype    = gen.chrom2geno(chromosomes)

        # Class assignments:
        Coil.lw_chromosomes = np.array(chromosomes)
        Coil.lw_genotype    = np.array(genotype)
        Coil.lw_homogeneity = mag.fitness_function(genotype, field_points, a)
