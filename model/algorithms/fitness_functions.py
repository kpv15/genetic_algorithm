import numpy as np

from model.elements import Individual


def count_nonzero_fitness_function(individual: Individual):
    fitness = 0
    for chromosome in individual.chromosomes.values():
        fitness += np.count_nonzero(chromosome.genes)
    return fitness
