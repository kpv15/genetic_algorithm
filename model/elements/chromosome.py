import math
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

    def replace(self, chromosome):
        self.genes = chromosome.genes

    def logical_not(self):
        return make_chromosome(np.logical_not(self.genes))

    def partial_logical_not(self, array: List[int]):
        return make_chromosome(np.array([~x if i in array else x for i, x in enumerate(self)]))

    def partial_logical_not_inplace(self, indexes):
        for index in range(len(self)):
            if index in indexes:
                self.genes[index] = ~self.genes[index]

    def logical_or(self, chromosome):
        return make_chromosome(np.logical_or(self.genes, chromosome.genes))

    def partial_logical_or(self, chromosome, array: List[int]):
        return make_chromosome(
            np.array([x or y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def logical_and(self, chromosome):
        return make_chromosome(np.logical_and(self.genes, chromosome.genes))

    def partial_logical_and(self, chromosome, array: List[int]):
        return make_chromosome(
            np.array([x and y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def logical_xor(self, chromosome):
        return make_chromosome(np.logical_xor(self.genes, chromosome.genes))

    def partial_logical_xor(self, chromosome, array: List[int]):
        return make_chromosome(
            np.array([x != y if i in array else x for i, (x, y) in enumerate(zip(self, chromosome))]))

    def combine(self, chromosome, function):
        return function(self, chromosome)

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

    def decode(self, precision: int):
        result = 0.0

        multiplier = 1
        for i in range(len(self) - 1 - precision, -1, -1):
            if self[i]:
                result += multiplier
            multiplier *= 2

        multiplier = 0.5
        for i in range(len(self) - precision, len(self)):
            if self[i]:
                result += multiplier
            multiplier /= 2

        return result


def make_chromosome(ndarray: np.ndarray) -> Chromosome:
    chromosome = Chromosome(ndarray.size)
    chromosome.genes = np.copy(ndarray.astype(np.bool_))
    return chromosome


def make_random_chromosome(size: int) -> Chromosome:
    chromosome = Chromosome(size)
    chromosome.genes = np.random.randint(0, 2, size, dtype=np.bool_)
    return chromosome


def make_real_chromosome(number: float, precision: int, fill: int) -> Chromosome:
    integer_part = int(number)
    float_part = number - integer_part
    genes = []

    while integer_part >= 1:
        genes.insert(0, 0 if integer_part % 2 == 0 else 1)
        integer_part = int(integer_part / 2)

    while fill - len(genes) - precision >= 1:
        genes.insert(0, 0)

    while precision > 0:
        genes.append(int(2 * float_part))
        precision -= 1

    chromosome = Chromosome(len(genes))
    chromosome.genes = np.asarray(genes)
    return chromosome


def chromosome_equal(first: Chromosome, second: Chromosome) -> bool:
    return np.array_equal(first.genes, second.genes)


def calculate_the_number_of_genes(number):
    genes_number = 0
    while number >= 1:
        number /= 2
        genes_number += 1

    return genes_number
