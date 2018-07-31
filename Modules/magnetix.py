import numpy as np
from scipy import constants as const

#TODO: incorporate radii into genotype

def __loop_field(transformed_genotype, a):
    """
    The exact B-field due to loop of wire at point z0 along axis.

    Input: Transformed genotype of coil, radius of loops (a).
    Output: B-field array of all contributions in [uT].

    Note: Must transform z-positions relative to z0 before supplying genotype.
    """

    z = np.array([c['z'] for c in transformed_genotype])
    I = np.array([c['I'] for c in transformed_genotype])

    numerator         = const.mu_0 * I * a**2
    denominator       = 2 * (a**2 + z**2)**(3/2)
    field_amt_array   = (numerator / denominator) * 1e6

    return field_amt_array # [uT]


def __genotype_transform(genotype, z0):
    """
    Transforms genotype from axial loop positions to axial distance of loops from z0. (z' = z - z0)

    Input: Genotype of coil, reference point (z0).
    Output: Transformed genotype.
    """

    transformed_genotype = [{'I' : c['I'], 'z' : z0 - c['z']} for c in genotype]

    return transformed_genotype


def __erf_homogeneity(genotype, hom_points, a):
    """
    Calculates homogeneity along axis of coil at certain points.

    Input: Genotype of coil, array of points to calculate at.
    Output: Homogeneity according to inverse error function.
    """

    centre_field    = magnetic_field(genotype, 0, a)
    normalization   = centre_field ** 2

    field_array     = field_along_axis(genotype, hom_points, a)
    variances       = (field_array[:,1] - centre_field) ** 2

    erf             = sum([x for x in variances]) / normalization
    homogeneity     = (1 / erf)

    return homogeneity


def magnetic_field(genotype, z0, a):
    """
    Calculates the total magnetic field at point z0 due to a genotype.

    Input: Genotype of coil, reference point (z0)
    Output: Scalar magnetic field at z0 in [uT]
    """

    transformed_genotype = __genotype_transform(genotype, z0)
    field_array          = __loop_field(transformed_genotype, a) # [uT]
    field_amt            = sum(field_array)

    return field_amt # [uT]


def field_along_axis(genotype, field_points, a):
    """
    Calculates field along axis of coil at certain points.

    Input: Genotype of coil, array of points to calculate at.
    Output: Array of B-fields, as well as the locations. [uT]

    Note: Calculation is done on only positive z-axis, but then values are mirrored since coil is symmetric.
    """

    # Preliminary calculations:
    field_number    = len(field_points)
    field_amounts   = np.array([magnetic_field(genotype, z, a) for z in field_points])

    # Building field_array:
    field_array         = np.zeros((field_number,2))
    field_array[:,0]    = field_points
    field_array[:,1]    = field_amounts

    # Flipping and stacking array to itself (since field is symmetric):
    field_array = np.vstack((np.flip(field_array, axis=0), field_array))

    # Changing sign of flipped z-values:
    field_array[:,0][:-field_number] = -field_array[:,0][:-field_number]

    return field_array


def average_field(genotype, field_points, a):
    """
    Calculates average field along axis of coil at certain points.

    Input: Genotype of coil, array of points to calculate at.
    Output: Scalar value of average B-field along specified axial points.
    """

    field_array     = field_along_axis(genotype, field_points, a)
    ave_field_amt   = np.average(field_array[:,1])

    return ave_field_amt # [uT]


def ppm_field(genotype, field_points, a):
    """
    Calculates PPM error field along axis of coil at certain points.

    Input: Genotype of coil, array of points to calculate at.
    Output: Array of PPM errors, as well as the locations.
    """

    field_array     = field_along_axis(genotype, field_points, a)
    centre_field    = magnetic_field(genotype, 0, a)

    numerator       = field_array[:,1] - centre_field
    denominator     = centre_field

    field_array[:,1] = (numerator / denominator) * 1e6
    ppm_field_array = field_array

    return ppm_field_array


def fitness_function(genotype, hom_points, a):
    """
    Calculates homogeneity based on arbitrary fitness function.

    Input: Genotype of coil, array of points to calculate at.
    Output: Fitness according to given fitness function.
    """

    fitness = __erf_homogeneity(genotype, hom_points, a)

    return fitness
