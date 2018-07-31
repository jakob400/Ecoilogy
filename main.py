import os

import Threading.threadcontrol as control
import Modules.writer as writer

if True:
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' =========================================== ')
    print('|-|   Ecoilogy: Version 1.1.4             |-|')
    print('|-|   Author: J Weirathmueller            |-|')
    print('|-|   Last Updated: July 31, 2018         |-|')
    print(' =========================================== \n\n')
    input('Press any button to begin...')


## TODO: Vectorize Population() methods
## TODO: Add function for random number generators (maybe, ask Dave).
## TODO: See why children update is slow (culprit is probably in crossover, time this as well).
## TODO: Check how taxing sorting of chromosomes is.
## TODO: Check FIXME's
## TODO: don't mutate AFTER children have been combined with parents, do it to new species only

mypop, application_runtime = control.launcher()

writer.results_output(mypop, application_runtime)
