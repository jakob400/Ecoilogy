import myconstants as myconst
from populationclass import *
from writer import *
import timeit

import genetix as mag

from pprint import pprint
import time


import threading
mainLoopFlag = True
epsilonFlag = False
Option = ''

## TODO: Vectorize Population() methods
## TODO: Add function for random number generators (maybe, ask Dave).
## TODO: See why children update is slow (culprit is probably in crossover, time this as well).
## TODO: Check how taxing sorting of chromosomes is.
## TODO: Check FIXME's
## TODO: don't mutate AFTER children have been combined with parents, do it to new species only



def timer():
    start = timeit.default_timer()
    pop = Population()
    end = timeit.default_timer()
    print('pop init is ', end-start)

    #for i in range(100):

    start = timeit.default_timer()
    pop.best_fitness_append()
    end = timeit.default_timer()
    print('append is ', end-start)

    start = timeit.default_timer()
    pop.parents_update()
    end = timeit.default_timer()
    print('parents is ', end-start)

    start = timeit.default_timer()
    pop.children_update()
    end = timeit.default_timer()
    print('children is ', end-start)

    start = timeit.default_timer()
    pop.mutate()
    end = timeit.default_timer()
    print('mutate is ', end-start)

    start = timeit.default_timer()
    pop.population_update()
    end = timeit.default_timer()
    print('pop update is', end-start)
    #print(i)
    print('Best Fitness is ', pop.best_fitness)


def run2():
    application_start = timeit.default_timer()

    pop = Population()

    pop.individuals[0].genotype_update()

    counter = 0
    last_difference = 0
    last_wait = 0
    global mainLoopFlag
    global epsilonFlag

    while mainLoopFlag:

        pop.individuals = pop.order(pop.individuals)

        pop.best_fitness_append()
        pop.parents_update()
        pop.children_update()
        pop.mutate()
        pop.population_update()

        pprint(gen.coil_order(pop.individuals[0].chromosomes))
        print('Best Fitness is:        ' + str(round(pop.best_fitness[-1],5)) + '\t\tEpsilon is ' + str(Coil.epsilon))
        print('Helmholtz fitness is:   ' + str(round(pop.individuals[0].hh_homogeneity,5)))
        print('Lee-Whiting fitness is: ' + str(round(pop.individuals[0].lw_homogeneity,5)))

        if (counter > 0):

            if (pop.best_fitness[-1] == pop.best_fitness[-2]):

                last_difference += 1

            if (pop.best_fitness[-1] != pop.best_fitness[-2]):

                last_difference = 0

                genotype_writer(pop.individuals[0].genotype)

        counter += 1
        print('Current Generation is: ', counter)
        print('Last difference was  : ', last_difference)


        if (last_difference == 0):

            last_wait = 0

        if ( last_difference > 20 and last_wait > 10):

            myconst.epsilon = myconst.epsilon * 0.01
            newEpsilon = myconst.epsilon
            pop.update_epsilon(newEpsilon)
            last_wait = 0
        last_wait += 1

        if epsilonFlag :

            pop.update_epsilon(float(input('What would you like the new value of epsilon to be?\n')))
            print("Successfully changed epsilon")
            epsilonFlag = False

    pprint(pop.individuals[0].genotype)
    application_end = timeit.default_timer()
    application_runtime = application_end - application_start
    results_output(copy.deepcopy(pop),application_runtime)


def get_input():
    global mainLoopFlag
    global epsilonFlag
    global Option

    # thread doesn't continue until key is pressed
    while mainLoopFlag:
        keystrk=input('Press a command then <ENTER> to stop... \n')
        if (keystrk == 'q'):
            print('You pressed \'q\'... Quitting')
            mainLoopFlag= False
        if (keystrk == 'z'):
            print('You pressed \'z\'... Changing z_epsilon')
            epsilonFlag = True

mainfoo = threading.Thread(target=run2)
controlfoo = threading.Thread(target=get_input)

mainfoo.start()
controlfoo.start()
