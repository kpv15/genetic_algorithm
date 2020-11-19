from math import exp, sqrt

import numpy as np
from typing import Dict

from model.elements import Individual


def count_nonzero_fitness_function(individual: Individual):
    fitness = 0
    for chromosome in individual.chromosomes.values():
        fitness += np.count_nonzero(chromosome.genes)
    return fitness


def _decoded_dict_to_numpy_array(decoded: Dict):
    return np.asarray([pair[1] for pair in sorted(decoded.items(), key=lambda x: x[0])])


def ackley_function(x: np.ndarray):
    a, b, c, d = 20, 0.2, 2 * np.pi, x.shape[0]
    return -a * exp(-b * sqrt((1/d) * np.sum(x**2))) - exp((1/d) * np.sum(np.cos(c*x))) + a + exp(1)


# remember to use functools.partial in order to bind precision to this function
def ackley_function_minimum_fitness_funtion(precision: Dict, individual: Individual):
    return -ackley_function(_decoded_dict_to_numpy_array(individual.decode(precision)))


# remember to use functools.partial in order to bind precision to this function
def ackley_function_maximum_fitness_funtion(precision: Dict, individual: Individual):
    return ackley_function(_decoded_dict_to_numpy_array(individual.decode(precision)))
