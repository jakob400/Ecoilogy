import os

import Threading.threadcontrol as control
import Modules.writer as writer
# import GUI.maingui as gui
import matplotlib.pyplot as plt




if True:
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' ========================================= ')
    print('|-|     Ecoilogy: Version 1.4.1         |-|')
    print('|-|     Author: J Weirathmueller        |-|')
    print('|-|     Last Updated: August 1, 2018    |-|')
    print(' ========================================= \n\n')
    input('Press <ENTER> to begin... ')
# import tkinter as tk
# root = tk.Tk()
# gui.parent()
## TODO: Vectorize Population() methods
## TODO: Add function for random number generators (maybe, ask Dave).
## TODO: See why children update is slow (culprit is probably in crossover, time this as well).
## TODO: Check how taxing sorting of chromosomes is.
## TODO: Check FIXME's
## TODO: Don't mutate AFTER children have been combined with parents, do it to new species only
## TODO: To make o.txt more reliable, maybe don't take from myconst, but instead take from pop.indivuduals[0] attributes
## TODO: Fix order in which information is displayed in threads.py. This may not be exactly representative of the actual last generation's attributes.
## TODO: Change homogeneity calculation to not allow ppm above certain range
## TODO: Plot initial best coil along with others at very end
## TODO: Create scheduler
## TODO: Figure out why class wide changes actually work for epsilon... it shouldn't







mypop, application_runtime = control.launcher()

writer.results_output(mypop, application_runtime)
writer.analytics_output(mypop.individuals[0].genotype)
