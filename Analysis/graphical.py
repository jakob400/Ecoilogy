import Modules.genetix as gen
import Modules.magnetix as mag
import Modules.myconstants as myconst

import matplotlib.pyplot as plt
import numpy as np

# Setting range of graphing:
show_points_number  = 1000 # Number of points on +ve z axis (double this to get total)
show_points         = np.linspace(0,1.0, show_points_number)
radius              = myconst.radius

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

    ext_genotype = genotype
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=radius))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=radius))

    ext_field   = mag.field_along_axis(ext_genotype, show_points, a=radius)
    lw_field    = mag.field_along_axis(lw_genotype, show_points, a=radius)
    hh_field    = mag.field_along_axis(hh_genotype, show_points, a=radius)

    ext_y = ext_field[:,1]
    lw_y = lw_field[:,1]
    hh_y = hh_field[:,1]

    x = lw_field[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')

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

    loop_number = len(genotype)

    ext_genotype = genotype
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=radius))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=radius))

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
    plt.ylabel('PPM Error')
    plt.legend()
    plt.grid()

    plt.savefig(address + '/PPM.png', dpi=400)

    plt.show()
    plt.clf()
    plt.close()

    return


def err_zoom_plot(address, genotype):

    loop_number = len(genotype)

    ext_genotype = genotype
    lw_genotype  = gen.chrom2geno(gen.lw_ChromGen(loop_number,radius=radius))
    hh_genotype  = gen.chrom2geno(gen.hh_ChromGen(loop_number,radius=radius))

    lw_error  = mag.ppm_field(lw_genotype, show_points, a=radius)
    hh_error  = mag.ppm_field(hh_genotype, show_points, a=radius)
    ext_error = mag.ppm_field(ext_genotype, show_points, a=radius)

    lw_y = lw_error[:,1]
    hh_y = hh_error[:,1]
    ext_y = ext_error[:,1]

    y_max = max(ext_y)
    x_max = 0.6

    x = lw_error[:,0]

    plt.plot(x, lw_y, label='Lee-Whiting' )
    plt.plot(x, hh_y, label='Helmholtz')
    plt.plot(x, ext_y, label='External')

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

    plt.hist(positions, bins=int(loop_number/2))
    plt.xlabel('z [m]')
    plt.ylabel('Turns')
    plt.title('Histogram of Loop Positions')

    plt.grid()
    plt.savefig(filename, dpi=400)
    plt.show()
    plt.clf()
    plt.close()

    return
