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

    def __len__(self):
        return self.genes.size

    def logical_not(self):
        return make_chromosome(np.logical_not(self.genes))

    def partial_logical_not(self, array: List[int]):
        return make_chromosome(np.array([not x if i in array else x for i, x in enumerate(self)]))

    def logical_or(self, chromosome):
        return make_chromosome(np.logical_or(self.genes, chromosome.genes))

    def partial_logical_or(self, chromosome, array: List[int]):
        return make_chromosome(np.array([x or y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def logical_and(self, chromosome):
        return make_chromosome(np.logical_and(self.genes, chromosome.genes))

    def partial_logical_and(self, chromosome, array: List[int]):
        return make_chromosome(np.array([x and y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def logical_xor(self, chromosome):
        return make_chromosome(np.logical_xor(self.genes, chromosome.genes))

    def partial_logical_xor(self, chromosome, array: List[int]):
        return make_chromosome(np.array([x != y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def combine(self, individual, function):
        return function(self, individual)

    def complete_to(self, chromosome):
        new_genes = np.empty(len(chromosome), np.bool_)
        new_genes[:len(self)] = self.genes
        new_genes[len(self):] = chromosome[len(self):]
        return make_chromosome(new_genes)

    def complete_to_random(self, chromosome):
        new_genes = np.empty(len(chromosome), np.bool_)
        new_genes[:len(self)] = self.genes
        new_genes[len(self):] = np.random.randint(0, 2, new_genes.size - len(self), np.bool_)
        return make_chromosome(new_genes)


def make_chromosome(ndarray: np.ndarray) -> Chromosome:
    chromosome = Chromosome(ndarray.size)
    chromosome.genes = np.copy(ndarray.astype(np.bool_))
    return chromosome


def make_random_chromosome(size: int) -> Chromosome:
    chromosome = Chromosome(size)
    chromosome.genes = np.random.randint(0, 2, size, dtype=np.bool_)
    return chromosome


def chromosome_equal(first: Chromosome, second: Chromosome) -> bool:
    return np.array_equal(first.genes, second.genes)
