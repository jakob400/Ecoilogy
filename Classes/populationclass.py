import random
import numpy as np
from scipy import constants as const
import copy

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



    def __init__(self):
        """Population initialization. Creates random set of coils."""

        self.individuals = copy.deepcopy([Coil() for _ in range(self.population_number)])
        self.order()

        Population.initial_best = self.individuals[0]

    def evolution_cycle(self):
        """
        Performs cycle operation on population to advance generation.

        Input: Population instance.
        Output: Population instance.
        """
        #TODO: Move this to populationclass

        self.order()
        self.parents_update()
        self.children_update()
        self.mutate()
        self.population_update()
        self.best_fitness_append()

        return


    def order(self):
        """Orders all individuals in the population according to fitness. (High to low.)"""

        self.individuals.sort(key=lambda x: x.fitness, reverse=True)


    def best_fitness_append(self):
        """
        Appends the fitness value of the most fit individual.
        (Assuming the population is already ordered)
        """

        self.best_fitness.append(self.individuals[0].fitness)


    def parents_update(self):
        """Updates list of parents and unfit."""

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
            children.append(crossover(parents[father_IDs[i]], parents[mother_IDs[i]], i)) ##FIXME: Change from append

        #self.children = self.order(copy.deepcopy(children)) #+ self.parents
        self.children = copy.deepcopy(children)


    def mutate(self):
        """Randomly mutates individuals in the children."""


        m = self.mutation_probability

        ## FIXME: try to vectorize
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



        self.individuals = copy.deepcopy(self.parents + self.children)
        self.order()


        # FIXME: This is a temporary fix. Find out why fitness is not being upated in the way you think it is.
        [c.genotype_update() for c in self.individuals]
        [c.field_update() for c in self.individuals]
        [c.fitness_update() for c in self.individuals]
        self.individuals = copy.deepcopy(self.individuals)
        self.order()


    def crossover(self, father, mother, i):
        """
        Performs random crossover between two individuals

        i: crossover number
        """
        ## FIXME: This may not be the best way to do crossover. Consider non-random method.
        ## FIXME: Ask Dave if this is the best implementation
        ## FIXME: Ask Dave if better to pass in entire object or just the attribute
        ## FIXME: Add child to population


        child = self.individuals[-(i+1)] # Picking from one of the unlucky, so a new instance of coil need not be created.
        fchromosomes = np.array(father.chromosomes)
        mchromosomes = np.array(mother.chromosomes)

        chrom_number = len(fchromosomes)

        # Breeding Types
        if (myconst.SPLIT == True):
            chromosomes = np.hstack((fchromosomes[:int(chrom_number/2)],mchromosomes[int(chrom_number/2):]))
        elif (myconst.RANDOM == True):
            father_probabilities = np.random.choice([True,False], size = chrom_number, p=[0.5,0.5])
            mother_probabilities = (father_probabilities != True) # Complement
            fchromosomes = fchromosomes[father_probabilities]
            mchromosomes = mchromosomes[mother_probabilities]
            chromosomes = np.hstack((fchromosomes,mchromosomes))

            #chromosomes = np.array(sorted(chromosomes, key=lambda k: k['z']))

            #pprint(chromosomes)
            #quit()

            #chromosomes = fchromosomes * father_probabilities + mchromosomes * mother_probabilities
        else:
            print("SYSTEM ERROR: BREEDING TYPE INVALID")
            exit()

        # child.manual_chromosomes_update(chromosomes)
        child.manual_chromosomes_update(chromosomes)

        return child # Replacing poor performers
