import Modules.genetix as gen
import Modules.magnetix as mag
import Modules.myconstants as myconst

import matplotlib.pyplot as plt
import numpy as np

show_points_number  = 1000 # Number of points on +ve z axis (double this to get total)
show_points         = np.linspace(0,1.0, show_points_number)
loop_number = 378

radius = myconst.radius

# init_genotype= Population.initial_best.genotype
lw_genotype  = gen.chrom2geno(gen.lw_perfectChromGen(loop_number,radius=radius))


# init_error= mag.ppm_field(init_genotype, show_points, a=radius)
lw_error  = mag.ppm_field(lw_genotype, show_points, a=radius)

lw_y = lw_error[:,1]

x = lw_error[:,0]

plt.plot(x, lw_y, label='Lee-Whiting' )

plt.title('PPM Error Field of L-W Coils')
plt.xlabel('z [m]')
plt.ylabel('PPM Error')
plt.legend()
plt.grid()

plt.show()
plt.clf()
