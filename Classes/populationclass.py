import random
import numpy as np
from scipy import constants as const
import copy
import Modules.genetix as gen

import Modules.myconstants as myconst
from Classes.coilclass import *


class Population:
    """Population object. Contains all individuals in population."""

    population_number = myconst.population_number

    parent_fraction = myconst.parent_fraction
    lucky_probability = myconst.lucky_probability
    mutation_probability = myconst.mutation_probability # probability that a child will be mutated

    best_fitness = []

    individuals = []
    parents = []
    unfit = []
    children = []
    epsilon_list = []

    initial_best = None

    initial_fitness_list = None

    realistic_chromosomes   = None
    realistic_genotype      = None
    realistic_fitness       = None



    def __init__(self):
        """Population initialization. Creates random set of coils."""

        self.individuals = copy.deepcopy([Coil() for _ in range(self.population_number)])
        self.order()

        Population.initial_best = self.individuals[0]
        Population.initial_fitness_list = [c.fitness for c in self.individuals]

    def evolution_cycle(self):
        """
        Performs cycle operation on population to advance generation.

        Input: Population instance.
        Output: Population instance.
        """

        self.order()
        self.parents_update()
        self.children_update()
        self.mutate()
        self.population_update()
        self.best_fitness_append()


    def order(self):
        """Orders all individuals in the population according to fitness. (High to low.)"""

        #print("Ordering population... \n")
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)


    def best_fitness_append(self):
        """
        Appends the fitness value of the most fit individual.
        (Assuming the population is already ordered)
        """

        self.best_fitness.append(self.individuals[0].fitness)


    def parents_update(self):
        """Updates list of parents and unfit."""


        #print("Updating list of parents... \n")
        s = self.parent_fraction
        l = self.lucky_probability

        fittest_number = int(s * len(self.individuals))

        # Choosing top "fittest_number" of individuals to be parents
        self.parents = [self.individuals[x] for x in range(fittest_number)]

        # Creating list of everyone else
        self.unfit = [self.individuals[x] for x in range(fittest_number,self.population_number)]

        for i in range(len(self.unfit)):

            if (random.uniform(0,1) < l):

                self.parents.append(self.unfit[i]) # Tacking on poor performers



    def children_update(self):
        """Updates list of children."""
        ## FIXME: try to vectorize
        ## NOTE: THIS IS THE SLOWEST LINK


        #print("Updating list of children... \n")
        crossover = self.crossover


        population_number = self.population_number
        parents = copy.deepcopy(self.parents)
        remainder = population_number - len(parents) # What's left after keeping parents


        father_IDs = np.random.randint(0,len(parents),remainder) # Exclusive upper limit
        mother_IDs = np.random.randint(0,len(parents),remainder)

        fathers = []
        mothers = []
        children = []
        for i in range(remainder):
            child = self.individuals[-(i+1)] # Picking from one of the unlucky, so a new instance of coil need not be created.
            children.append(crossover(parents[father_IDs[i]], parents[mother_IDs[i]], child)) ##FIXME: Change from append

        #self.children = self.order(copy.deepcopy(children)) #+ self.parents
        self.children = copy.deepcopy(children)


    def mutate(self):
        """Randomly mutates individuals in the children."""


        #print("Mutating individuals in list of children... \n")
        m = self.mutation_probability

        for i in range(len(self.children)):

            if (random.uniform(0,1) < m):

                self.children[i].mutate()

    def update_epsilon(self, newEpsilon):
        Coil.epsilon = newEpsilon

    def update_z_max(self, newZ_max):
        # TODO: FINISH Me
        Coil.z_max = newZ_max

    def population_update(self):
        """Updates population."""

        #print("Updating population... \n")
        self.individuals = copy.deepcopy(self.parents + self.children)
        self.order()

        # FIXME: This is a temporary fix. Find out why fitness is not being upated in the way you think it is.
        [c.genotype_update() for c in self.individuals]
        [c.field_update() for c in self.individuals]
        [c.fitness_update() for c in self.individuals]
        self.individuals = copy.deepcopy(self.individuals)
        self.order()


    def crossover(self, father, mother, child):
        """
        Performs random crossover between two individuals

        i: crossover number
        """

        fchromosomes = np.array(father.chromosomes)
        mchromosomes = np.array(mother.chromosomes)
        chrom_number = len(fchromosomes)

        # Breeding Types

        if (myconst.RANDOM == True):
            father_probabilities = np.random.choice([True,False], size = chrom_number, p=[0.5,0.5])
            mother_probabilities = (father_probabilities != True) # Complement
            fchromosomes = fchromosomes[father_probabilities]
            mchromosomes = mchromosomes[mother_probabilities]
            chromosomes = np.hstack((fchromosomes,mchromosomes))
        else:
            print("SYSTEM ERROR: BREEDING TYPE INVALID")
            exit()

        # child.manual_chromosomes_update(chromosomes)
        child.manual_chromosomes_update(chromosomes)

        return child # Replacing poor performers

    def bestRealisticize(self):

        self.order() # Maybe unnecessary but I'm too lazy to check if it's redundant

        chromosomes     = self.individuals[0].chromosomes

        mill_precision  = myconst.mill_precision
        wire_width      = myconst.wire_width
        wall_width      = myconst.wall_width
        max_stack       = myconst.max_stack
        r_min           = myconst.r_min

        self.realistic_chromosomes  = gen.chromRealisticize(chromosomes, mill_precision, wire_width, wall_width, max_stack, r_min)
        self.realistic_genotype     = gen.chrom2geno(self.realistic_chromosomes)
        self.realistic_fitness      = mag.fitness_function(self.realistic_genotype, None)
