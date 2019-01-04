import numpy as np

import Analysis.graphical as g
import Modules.genetix as gen

address = 'Output/Thursday16.16:23:23@10/'

def genotype_extractor():
    destination = address + 'chromloc.txt'
    ext_positions = np.genfromtxt(destination)
    ext_chromosomes = [{'z' : z, 'I' : 1, 'r': 0.25} for z in ext_positions]
    ext_genotype = gen.chrom2geno(ext_chromosomes)
    loop_number = len(ext_genotype)
    return ext_genotype


genotype = genotype_extractor()


g.err_plot(address, genotype)
g.err_zoom_plot(address, genotype)
g.field_plot(address, genotype)
g.hist_plot(address, genotype)
