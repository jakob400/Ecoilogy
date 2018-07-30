import myconstants as myconst

import numpy as np

import os
import time
import datetime
from decimal import Decimal
import pickle

now = datetime.datetime.now()

destination = 'Output/'
#time_name = now.strftime('%A%d') + 'BF:' + "{:.2E}".format(Decimal(pop.individuals[0].fitness))
time_name = now.strftime('%A%d.%X')
important_params = '@' + str(myconst.calc_points)
new_directory = destination + time_name + important_params
genotype_directory = 'Output/' + time_name + important_params + '/pickles'

os.mkdir(new_directory)
os.mkdir(genotype_directory)


def genotype_writer(genotype):
    filename = genotype_directory + '/'

    i = 0
    while True:
        write_filename = filename + str(i) + '.pic'
        if (os.path.exists(write_filename)):
            i += 1
        if not (os.path.exists(write_filename)):
            #np.savetxt(write_filename, np.array(genotype), delimiter=',', fmt='%s')
            f = open(write_filename, "wb")
            pickle.dump(genotype, f)
            f.close()
            break


def results_output(pop,runtime):

    filename1 = 'Output/' + time_name + important_params + '/o.txt'

    f = open(filename1, "w")

    neat_date = now.strftime("%A %d. %B %Y")
    f.write('Finished computation at ' + str(neat_date) +'.\n')
    f.write('Generations                      =       '+ str(len(pop.best_fitness)) + '\n')
    f.write('Final best fitness               =       '+ str(pop.individuals[0].fitness)+'\n')
    f.write('RUNTIME                          =       '+ str(runtime) + '\n\n\n')

    f.write('PILEUP                           =       '+ str(myconst.PILEUP) + '\n')
    f.write('REFLECTION                       =       '+ str(myconst.REFLECTION) + '\n')
    f.write('REDRAW                           =       '+ str(myconst.REDRAW) + '\n')
    f.write('SPREADOUT                        =       '+ str(myconst.SPREADOUT) + '\n')
    f.write('loop_number                      =       '+ str(myconst.loop_number) + '\n')
    f.write('z_min                            =       '+ str(myconst.z_min) + '\n')
    f.write('z_max                            =       '+ str(myconst.z_max) + '\n')
    f.write('radius                           =       '+ str(myconst.radius) + '\n')


    f.write('calc_z_min                       =       '+ str(myconst.calc_z_min) + '\n')
    f.write('calc_z_max                       =       '+ str(myconst.calc_z_max) + '\n')
    f.write('calc_points                      =       '+ str(myconst.calc_points) + '\n')
    f.write('init_fitness                     =       '+ str(myconst.init_fitness) + '\n')

    f.write('epsilon                          =       '+ str(myconst.epsilon) + '\n')
    f.write('population_number                =       '+ str(myconst.population_number) + '\n')
    f.write('parent_fraction                  =       '+ str(myconst.parent_fraction) + '\n')
    f.write('lucky_probability                =       '+ str(myconst.lucky_probability) + '\n')
    f.write('mutation_probability             =       '+ str(myconst.mutation_probability) + '\n')
    f.write('max_fitness (threshold)          =       '+ str(myconst.max_fitness) + '\n')
    f.write('B_ave_multiplier                 =       '+ str(myconst.B_ave_multiplier))

    f.close()





    filename2 = 'Output/' + time_name + important_params + '/chrom.txt'
    #f = open(filename2, "w")
    #f.write(str(pop.individuals[0].chromosomes))
    np.savetxt(filename2, np.array(pop.individuals[0].chromosomes), delimiter=',', fmt='%s')


    filename3 = 'Output/' + time_name + important_params + '/generations.txt'
    np.savetxt(filename3, pop.best_fitness, delimiter=',')

    filename4 = 'Output/' + time_name + important_params + '/chromloc.txt'
    np.savetxt(filename4, np.array([x['z'] for x in pop.individuals[0].chromosomes]), delimiter=',', fmt='%s')
