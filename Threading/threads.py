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


def evolver(queueop, mypop, application_runtime):

    application_start = timeit.default_timer()

    pop = Population()

    #pop.individuals[0].genotype_update()

    generation = 0
    last_wait = 0
    last_difference = 0

    global mainLoopFlag
    global epsilonFlag

    pop.update_epsilon(gen.epsilonCalc(last_difference, generation))


    while mainLoopFlag:

        # Cycling the population through one evolutionary generation
        pop.evolution_cycle()
        if (len(pop.best_fitness) > 1):
            last_difference = gen.last_difference_calc(pop.best_fitness)
        generation += 1

        pop.update_epsilon(gen.epsilonCalc(last_difference, generation))

        # pprint(gen.coil_order(pop.individuals[0].chromosomes))


        #TODO: Have parameter for fractional fitness. In other words, have best_fitness/best_accepted_fitness, where best_accepted_fitness is chosen from the best of the analytic solutions.
        print('Current Generation is        : ', generation)
        print('Last difference was          : ', last_difference)
        print('Epsilon is                   : ' + str(Coil.epsilon))
        print('Initial best fitness is      : ' + str(round(Population.initial_best.fitness, 5)))
        print('Best Fitness is              : ' + str(round(pop.best_fitness[-1],5)))
        print('Helmholtz fitness is         : ' + str(round(pop.individuals[0].hh_homogeneity,5)))
        print('9/4 Lee-Whiting fitness is   : ' + str(round(pop.individuals[0].lwb_homogeneity,5)))
        print('Lee-Whiting fitness is       : ' + str(round(pop.individuals[0].lw_homogeneity,5)))
        print('Solenoid fitness is          : ' + str(round(pop.individuals[0].sol_homogeneity,5)))
        print('Gapped Solenoid fitness is   : ' + str(round(pop.individuals[0].gap_homogeneity,5)))

        print('\n')

        writer.genotype_writer(pop.individuals[0].genotype)

        if(Coil.epsilon < 1e-7):
            mainLoopFlag = False
            break


    application_end = timeit.default_timer()

    application_runtime = application_end - application_start

    pop.bestRealisticize()


    print('Best Fitness is              : ' + str(round(pop.best_fitness[-1],5)))
    print('Realistic Fitness is         : ' + str(round(pop.realistic_fitness,5)))


    mypop = copy.deepcopy(pop)

    queueop.put((mypop, application_runtime))


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
