from typing import List

import numpy as np


class Chromosome:
    __slots__ = "genes"

    def __init__(self, size: int):
        self.genes = np.empty(size, np.bool_)

    def __getitem__(self, item):
        return self.genes[item]

    def __setitem__(self, key, value):
        self.genes[key] = value

    def size(self) -> int:
        return self.genes.size

    def logical_not(self):
        return make_chromosome(np.logical_not(self.genes))

    def partial_logical_not(self, array: List[int]):
        return make_chromosome(np.array([not x if i in array else x for i, x in enumerate(self)]))

    def logical_or(self, chromosome):
        return make_chromosome(np.logical_or(self.genes, chromosome.genes))

    def partial_logical_or(self, chromosome, array):
        return make_chromosome(np.array([x or y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def logical_and(self, chromosome):
        return make_chromosome(np.logical_and(self.genes, chromosome.genes))

    def partial_logical_and(self, chromosome, array):
        return make_chromosome([x and y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))])

    def combine(self, individual, function):
        return function(self, individual)

    def complete_to(self, chromosome):
        new_genes = np.empty(chromosome.size(), np.bool_)
        new_genes[:self.size()] = self.genes
        new_genes[self.size():] = chromosome[self.size():]
        return make_chromosome(new_genes)

    def complete_to_random(self, chromosome):
        new_genes = np.empty(chromosome.size(), np.bool_)
        new_genes[:self.size()] = self.genes
        new_genes[self.size():] = np.random.randint(0, 2, new_genes.size - self.size(), np.bool_)
        return make_chromosome(new_genes)


def make_chromosome(array):
    chromosome = Chromosome(len(array))
    chromosome.genes = np.copy(array)
    return chromosome


def chromosome_equal(chromosome1: Chromosome, chromosome2: Chromosome) -> bool:
    return np.array_equal(chromosome1.genes, chromosome2.genes)
