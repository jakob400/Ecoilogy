import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
import imageio

root_path = 'Output/Friday27.14:33:33@10/'

input_folder = root_path + 'pickles/'
png_folder = root_path + 'genotypes/'


genotype_list = []



def pickle_grabber():
    os.mkdir(png_folder)
    i = 0

    while True:
        filename = input_folder + str(i) + '.pic'
        if (os.path.exists(filename)):
            file = open(filename, 'rb')
            genotype = pickle.load(file)

            file.close()

            zeros = np.zeros(genotype.shape) # FIXME: Fix later to be faster
            z = [c['z'] for c in genotype]
            plt.scatter(z,zeros, s=0.5)
            plt.savefig(png_folder + str(i) + '.png', dpi = 400)
            plt.clf()

            i += 1
        elif not (os.path.exists(filename)):
            break
    return




def waterfall_gen():
    # TODO: Change colour based on homogeneity
    i = 0
    while True:
        filename = input_folder + str(i) + '.pic'
        if (os.path.exists(filename)):
            file = open(filename, 'rb')
            genotype_list.append(pickle.load(file))
            file.close()
            i += 1
        else:
            break

    j = 0 # Counter for generation (roughly)
    for genotype in genotype_list:
        z = [c['z'] for c in genotype]
        y = np.zeros(genotype.shape) - j
        plt.scatter(z, y, color = 'black',  s = 0.05)
        j += 1

    plt.title('Evolution of Coil Windings')
    plt.xlabel('z [m]')
    plt.ylabel('-Generation')
    plt.grid(linewidth=0.1)
    plt.legend()
    plt.savefig(root_path + 'waterfall.png', dpi = 1000)
    plt.clf()




def animator():
    images = []
    filenames = []

    i = 0
    while True:
        name = png_folder + str(i) + '.png'
        if (os.path.exists(name)):
            filenames.append(name)
            print(i)
            i+=1
        else:
            break

    for filename in filenames:
        print(filename)
        images.append(imageio.imread(filename))
    imageio.mimsave(root_path + 'animation.gif', images)

#pickle_grabber()
#animator()
waterfall_gen()
