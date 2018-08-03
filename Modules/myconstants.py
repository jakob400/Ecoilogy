# Plotting Mode
GRAPHICAL = False

# Mutation Methods:
# 1. 'PILEUP'
# 2. 'REFLECTION'
# 3. 'REDRAW'
# 4. 'SPREADOUT' = False # Broken
MutationScheme = 'REFLECTION'

# Breeding Method:
RANDOM = True # FIXME: Currently broken method
SPLIT = False

#TODO: Write conditional here to check if more than one breeding method or mutation method are active.


radius = 0.25

loop_number = 100 # Keep this an even number #TOTAL number of loops
z_min = 0
z_max = 0.5
epsilon = 0.1 # Distance of mutation

I_min = 1.0
I_max = 1.0
I_epsilon = 0.0

# Defining range of homogeneity calculation
calc_z_min = 0
calc_z_max = 0.25
calc_points = 10

init_fitness = 0



population_number = 100

parent_fraction = 0.1
lucky_probability = 0.05
mutation_probability = 0.1 # probability that a child will be mutated

max_fitness = 324300000


B_ave_multiplier = 1#10
fitness_multiplier = 1#e6
