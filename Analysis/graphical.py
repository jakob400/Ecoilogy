import Modules.genetix as gen
import Modules.magnetix as mag
import Modules.myconstants as myconst

import matplotlib.pyplot as plt
import numpy as np

from Classes.populationclass import *

# Setting range of graphing:
show_points_number  = 1000 # Number of points on +ve z axis (double this to get total)
show_points         = np.linspace(0,1.0, show_points_number)
radius              = myconst.r_0
gap_precision       = myconst.gap_precision

def waterfall_plot(address, history):
    # TODO: Change colour based on homogeneity
    j = 0 # Counter for generation (roughly)
    for genotype in history:
        z = [c['z'] for c in genotype]
        y = np.zeros(genotype.shape) - j
        plt.scatter(z, y, color = 'black',  s = 0.05)
        j += 1

    plt.title('Evolution of Coil Windings')
    plt.xlabel('z [m]')
    plt.ylabel('-Generation')

    plt.grid(linewidth=0.1)
    plt.legend()
    plt.savefig(address + '/waterfall.png', dpi = 1000)
    plt.clf()

    return


# def evol_history_plot(address, best_fitness_list):


def field_plot(address, genotype):
    loop_number = len(genotype)
    # loop_z_max = genotype[-1]['z']
    # r_min      = sorted(genotype, key=lambda k: k['r'])[0]['r']
    r_0             = myconst.r_0
    r_min           = myconst.r_min
    r_max           = myconst.r_max
    mill_precision  = myconst.mill_precision
    loop_z_max      = myconst.z_max

    ext_genotype = genotype

    # init_genotype= Population.initial_best.genotype
    # lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=r_min))
    # lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(loop_number,radius=r_min))
    # hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=r_min))
    # sol_genotype = gen.chrom2geno(gen.sol_ChromGen(loop_number,loop_z_max=loop_z_max, radius=r_min))
    # gap_genotype = gen.chrom2geno(gen.gap_ChromGen(r_min, loop_z_max, loop_number, gap_precision))
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(genotype,r_0))
    lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(genotype,r_0))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(genotype,r_0))
    sol_genotype = gen.chrom2geno(gen.sol_ChromGen(genotype,loop_z_max=loop_z_max, std_radius=r_0))
    gap_genotype = gen.chrom2geno(gen.gap_ChromGen(genotype,r_0,length=loop_z_max, precision=mill_precision))

    # init_field  = mag.field_along_axis(init_genotype,show_points, a=radius)
    ext_field   = mag.field_along_axis(ext_genotype, show_points)
    lw_field    = mag.field_along_axis(lw_genotype, show_points)
    lwb_field   = mag.field_along_axis(lwb_genotype, show_points)
    hh_field    = mag.field_along_axis(hh_genotype, show_points)
    sol_field   = mag.field_along_axis(sol_genotype, show_points)
    gap_field   = mag.field_along_axis(gap_genotype, show_points)

    ext_y = ext_field[:,1]
    lw_y = lw_field[:,1]
    lwb_y = lw_field[:,1]
    hh_y = hh_field[:,1]
    sol_y = sol_field[:,1]
    gap_y = gap_field[:,1]
    # init_y = init_field[:,1]

    x = lw_field[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, lwb_y, label='9/4 Lee-Whiting')
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')
    plt.plot(x, sol_y, label='Solenoid')
    plt.plot(x, gap_y, label='Gapped Solenoid')
    # plt.plot(x, init_y, label = 'Initial')

    plt.title('Magnetic Field Strengths of Competing Coils')
    plt.xlabel('z [m]')
    plt.ylabel('|B| [$\\mu$T]')
    plt.legend()

    plt.grid()
    plt.savefig(address + '/Fields.png', dpi=400)
    plt.show()
    plt.clf()
    plt.close()

    return


def err_plot(address, genotype):
    r_0             = myconst.r_0
    mill_precision  = myconst.mill_precision
    loop_z_max      = myconst.z_max

    loop_number = len(genotype)
    # loop_z_max = genotype[-1]['z']
    r_min      = sorted(genotype, key=lambda k: k['r'])[0]['r']

    ext_genotype = genotype
    # init_genotype= Population.initial_best.genotype
    # lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=r_min))
    # lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(loop_number,radius=r_min))
    # hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=r_min))
    # sol_genotype = gen.chrom2geno(gen.sol_ChromGen(loop_number,loop_z_max=loop_z_max, radius=r_min))
    # gap_genotype = gen.chrom2geno(gen.gap_ChromGen(r_min,loop_z_max, loop_number, gap_precision))
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(genotype,r_0))
    lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(genotype,r_0))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(genotype,r_0))
    sol_genotype = gen.chrom2geno(gen.sol_ChromGen(genotype,loop_z_max=loop_z_max, std_radius=r_0))
    gap_genotype = gen.chrom2geno(gen.gap_ChromGen(genotype,r_0,length=loop_z_max, precision=mill_precision))

    # init_error= mag.ppm_field(init_genotype, show_points, a=radius)
    lw_error  = mag.ppm_field(lw_genotype, show_points)
    lwb_error = mag.ppm_field(lwb_genotype, show_points)
    hh_error  = mag.ppm_field(hh_genotype, show_points)
    ext_error = mag.ppm_field(ext_genotype, show_points)
    sol_error = mag.ppm_field(sol_genotype, show_points)
    gap_error = mag.ppm_field(gap_genotype, show_points)

    lw_y = lw_error[:,1]
    lwb_y = lw_error[:,1]
    hh_y = hh_error[:,1]
    ext_y = ext_error[:,1]
    sol_y = sol_error[:,1]
    gap_y = gap_error[:,1]
    # init_y = init_error[:,1]

    x = lw_error[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, lwb_y, label='9/4 Lee-Whiting')
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')
    plt.plot(x, sol_y, label='Solenoid')
    plt.plot(x, gap_y, label='Gapped Solenoid')
    # plt.plot(x, init_y, label = 'Initial')

    plt.title('PPM Error Fields of Competing Coils')
    plt.xlabel('z [m]')
    plt.ylabel('PPM Error')
    plt.legend()
    plt.grid()

    plt.savefig(address + '/PPM.png', dpi=400)

    plt.show()
    plt.clf()
    plt.close()

    return


def err_zoom_plot(address, genotype):
    r_0             = myconst.r_0
    mill_precision  = myconst.mill_precision
    loop_z_max      = myconst.z_max

    loop_number = len(genotype)
    # loop_z_max = genotype[-1]['z']
    r_min      = sorted(genotype, key=lambda k: k['r'])[0]['r']

    ext_genotype = genotype
    # init_genotype= Population.initial_best.genotype
    # lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=r_min))
    # lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(loop_number, r_min))
    # hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=r_min))
    # sol_genotype = gen.chrom2geno(gen.sol_ChromGen(loop_number,loop_z_max=loop_z_max, radius=r_min))
    # gap_genotype = gen.chrom2geno(gen.gap_ChromGen(r_min, loop_z_max, loop_number, gap_precision))
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(genotype,r_0))
    lwb_genotype = gen.chrom2geno(gen.lwb_ChromGen(genotype,r_0))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(genotype,r_0))
    sol_genotype = gen.chrom2geno(gen.sol_ChromGen(genotype,loop_z_max=loop_z_max, std_radius = r_0))
    gap_genotype = gen.chrom2geno(gen.gap_ChromGen(genotype,r_0,length=loop_z_max, precision=mill_precision))

    # init_error= mag.ppm_field(init_genotype, show_points, a=radius)
    lw_error  = mag.ppm_field(lw_genotype, show_points)
    lwb_error = mag.ppm_field(lwb_genotype, show_points)
    hh_error  = mag.ppm_field(hh_genotype, show_points)
    ext_error = mag.ppm_field(ext_genotype, show_points)
    sol_error = mag.ppm_field(sol_genotype, show_points)
    gap_error = mag.ppm_field(gap_genotype, show_points)

    # init_y= init_error[:,1]
    lw_y = lw_error[:,1]
    lwb_y = lwb_error[:,1]
    hh_y = hh_error[:,1]
    ext_y = ext_error[:,1]
    sol_y = sol_error[:,1]
    gap_y = gap_error[:,1]

    y_max = max(ext_y)
    x_max = 0.6

    x = lw_error[:,0]


    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, lwb_y, label='9/4 Lee-Whiting')
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')
    plt.plot(x, sol_y, label='Solenoid')
    plt.plot(x, gap_y, label='Gapped Solenoid')
    # plt.plot(x, init_y, label = 'Initial')

    plt.ylim(-y_max, y_max)
    plt.xlim(-x_max, x_max)

    plt.title('PPM Error Fields of Competing Coils (zoomed)')
    plt.xlabel('z [m]')
    plt.ylabel('PPM Error')
    plt.legend()
    plt.grid()

    plt.savefig(address + '/PPM_zoom.png', dpi=600)

    plt.show()
    plt.clf()
    plt.close()

    return


def hist_plot(address, genotype):

    loop_number = len(genotype)

    filename = address + '/hist.png'
    positions = [c['z'] for c in genotype]

    plt.hist(positions, bins=1000)
    plt.xlabel('z [m]')
    plt.ylabel('Turns')
    plt.title('Histogram of Loop Positions')

    plt.grid()
    plt.savefig(filename, dpi=400)
    plt.show()
    plt.clf()
    plt.close()

    return
