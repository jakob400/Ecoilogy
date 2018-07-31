import timeit

import Modules.myconstants as myconst
import Modules.magnetix as mag
import Modules.genetix as gen
import Modules.writer as writer

from Classes.populationclass import *


from pprint import pprint
import time


import threading
mainLoopFlag = True
epsilonFlag = False
Option = ''

mypop = None
application_runtime = None


if True:
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' =========================================== ')
    print('|-|   Ecoilogy: Version 1.1.2             |-|')
    print('|-|   Author: J Weirathmueller            |-|')
    print('|-|   Last Updated: July 31, 2018         |-|')
    print(' =========================================== \n\n')
    input('Press any button to begin...')


## TODO: Vectorize Population() methods
## TODO: Add function for random number generators (maybe, ask Dave).
## TODO: See why children update is slow (culprit is probably in crossover, time this as well).
## TODO: Check how taxing sorting of chromosomes is.
## TODO: Check FIXME's
## TODO: don't mutate AFTER children have been combined with parents, do it to new species only

def evolver():
    global mypop
    global application_runtime


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

        pop.parents_update()
        pop.children_update()
        pop.mutate()
        pop.population_update()
        pop.best_fitness_append()

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
    #results_output(copy.deepcopy(pop),application_runtime)
    mypop = copy.deepcopy(pop)


def get_input():
    global mainLoopFlag
    global epsilonFlag
    global Option

    # thread doesn't continue until key is pressed
    while mainLoopFlag:
        keystrk=input('Press a command then <ENTER> to modify/stop run... \n')
        if (keystrk == 'q'):
            print('You pressed \'q\'... Quitting')
            mainLoopFlag= False
            break
        if (keystrk == 'z'):
            print('You pressed \'z\'... Changing z_epsilon')
            epsilonFlag = True

# Defining threads:
mainfoo = threading.Thread(target=evolver)
controlfoo = threading.Thread(target=get_input)

## Launching threads:
mainfoo.start()
controlfoo.start()

## Waiting for threads to terminate:
mainfoo.join()
controlfoo.join()


writer.results_output(mypop, application_runtime)
