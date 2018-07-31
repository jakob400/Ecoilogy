import timeit
from pprint import pprint
import copy

import Modules.myconstants as myconst
import Modules.magnetix as mag
import Modules.genetix as gen
import Modules.writer as writer

from Classes.populationclass import *

mainLoopFlag = True
epsilonFlag = False

def evolver(myq, mypop, application_runtime):

    application_start = timeit.default_timer()

    pop = Population()

    pop.individuals[0].genotype_update()

    counter = 0
    last_wait = 0
    last_difference = 0

    global mainLoopFlag
    global epsilonFlag

    while mainLoopFlag:
        if epsilonFlag :
            pop.update_epsilon(float(input('What would you like the new value of epsilon to be?\n')))
            print("Successfully changed epsilon")
            epsilonFlag = False

        pop = gen.evolution_cycle(pop)
        if (counter > 0):
            last_difference = gen.last_difference_calc(pop.best_fitness)

        pprint(gen.coil_order(pop.individuals[0].chromosomes))

        print('Current Generation is: ', counter)
        print('Last difference was  : ', last_difference)
        print('Best Fitness is:        ' + str(round(pop.best_fitness[-1],5)) + '\t\tEpsilon is ' + str(Coil.epsilon))
        print('Helmholtz fitness is:   ' + str(round(pop.individuals[0].hh_homogeneity,5)))
        print('Lee-Whiting fitness is: ' + str(round(pop.individuals[0].lw_homogeneity,5)))




        writer.genotype_writer(pop.individuals[0].genotype)

        counter += 1




    pprint(pop.individuals[0].genotype)
    application_end = timeit.default_timer()

    application_runtime = application_end - application_start
    mypop = copy.deepcopy(pop)

    myq.put((mypop, application_runtime))


def get_input():
    global mainLoopFlag
    global epsilonFlag

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
