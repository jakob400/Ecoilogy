import numpy as np
import math
from scipy import constants as const
import matplotlib.pyplot as plt

import magnetix as mag
import genetix as gen


#TODO: Write in capacity to mark where calc_z_max from original GA was
#TODO: Allow reading in of pickles instead of chromloc


# Taking input to set range of homogeneity calculation:
calc_z_max  = float(input("Enter z_max       :"))
calc_points = int(input("Enter calc_points :"))
radius           = float(input("Enter radius of loops: "))


# Setting more global variables:
folder = 'Output/Monday30.16:53:54@10/'
zlist       = np.linspace(0,calc_z_max,calc_points)
a           = 0.25   # Radius of coil
loop_number = None # To be changed by input file



# Setting range of graphing:
show_points_number = 1000 # Number of points on +ve z axis (double this to get total)
show_points = np.linspace(0,1.0, show_points_number)


def ext_init(): # Reads in data

    global loop_number
    destination1 = folder + 'chromloc.txt'
    ext_positions = np.genfromtxt(destination1)
    ext_chromosomes = [{'z' : z, 'I' : 1} for z in ext_positions]
    ext_genotype = gen.chrom2geno(ext_chromosomes)
    loop_number = len(ext_genotype)

    return ext_genotype


def genotype_histogrammer(genotype):
    filename = folder + 'hist.png'
    positions = [c['z'] for c in genotype]

    plt.hist(positions, bins=50)
    plt.xlabel('z [m]')
    plt.ylabel('Counts')
    plt.title('Histogram of Loop Positions')

    plt.grid()
    plt.savefig(filename, dpi=400)
    plt.show()
    plt.clf()
    plt.close()


def field_plotter():
    """ Plots the magnetic field along the axis """
    lw_field    = mag.field_along_axis(lw_genotype, show_points, a=radius)
    hh_field    = mag.field_along_axis(hh_genotype, show_points, a=radius)
    ext_field   = mag.field_along_axis(ext_genotype, show_points, a=radius)

    lw_y = lw_field[:,1]
    hh_y = hh_field[:,1]
    ext_y = ext_field[:,1]

    x = lw_field[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')

    plt.title('Magnetic Field Strengths of Competing Coils')
    plt.xlabel('z [m]')
    plt.ylabel('|B| [$\\mu$T]')
    plt.legend()

    plt.grid()
    plt.savefig(folder + 'Fields.png', dpi=400)
    plt.show()
    plt.clf()
    plt.close()


def err_plotter():
    """ Plots the ppm error field along the axis """
    lw_error  = mag.ppm_field(lw_genotype, show_points, a=radius)
    hh_error  = mag.ppm_field(hh_genotype, show_points, a=radius)
    ext_error = mag.ppm_field(ext_genotype, show_points, a=radius)

    lw_y = lw_error[:,1]
    hh_y = hh_error[:,1]
    ext_y = ext_error[:,1]

    x = lw_error[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')

    plt.title('PPM Error Fields of Competing Coils')
    plt.xlabel('z [m]')
    plt.ylabel('|B| [$\\mu$T]')
    plt.legend()
    plt.grid()

    plt.savefig(folder + 'PPM.png', dpi=400)

    plt.show()
    plt.clf()
    plt.close()



def fitness_printer():

    ext_fitness = mag.fitness_function(ext_genotype, zlist, a=radius)
    print('External    :', ext_fitness)

    lw_fitness  = mag.fitness_function(lw_genotype, zlist, a=radius)
    print('Lee-Whiting :', lw_fitness)

    hh_fitness  = mag.fitness_function(hh_genotype, zlist, a=radius)
    print('Helmholtz   :', hh_fitness)


# Initializing genotypes
ext_genotype = ext_init() # Must be first as this sets loop_number
lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=radius))
hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=radius))

genotype_histogrammer(ext_genotype)
fitness_printer()
field_plotter()
err_plotter()
