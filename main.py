import os

import Threading.threadcontrol as control
import Modules.writer as writer
# import GUI.maingui as gui
import matplotlib.pyplot as plt




if True:
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' ========================================= ')
    print('|-|     Ecoilogy: Version 2.0.0         |-|')
    print('|-|     Author: J Weirathmueller        |-|')
    print('|-|     Last Updated: January 4, 2019   |-|')
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

## TODO: Have wire thickness be input parameter - also dictates wires piling up (1mm is good start)
## TODO: Pickle initial_best
## TODO: Use eq. 3 in solenoid gap paper
## TODO: Use same positions as normal solenoid, with centre cut out. Normalize remaining wires to have same total current
## TODO: Try old fitness function, but increase exponent to be harder on larger deviations
## TODO: Add master file  for all the standards chromosomes
## TODO: Figure out why 9/4 lee whiting looks the same as exact lee whiting







mypop, application_runtime = control.launcher()

writer.results_output(mypop, application_runtime)
#writer.analytics_output(mypop.individuals[0].genotype)
