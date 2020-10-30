from functools import reduce
from typing import List

from .individual import Individual


class Population:
    __slots__ = "individuals"

    def __init__(self):
        self.individuals = []

    def __getitem__(self, item):
        return self.individuals[item]

    def __setitem__(self, key, value):
        self.individuals[key] = value

    def __len__(self):
        return len(self.individuals)

    def all_indexes(self) -> List[int]:
        return [i for i in range(len(self))]

    def append(self, individual: Individual):
        self.individuals.append(individual)

    def extend(self, *args):
        self.individuals.extend(args)

    def remove(self, indexes: List[int]):
        for i in reversed(sorted(indexes)):
            if i < len(self):
                del self.individuals[i]

    def reduce(self, indexes: List[int], function) -> Individual:
        to_reduce = []
        for i in indexes:
            if i < len(self):
                to_reduce.append(self[i])
        return reduce(function, to_reduce)


def make_population(*args) -> Population:
    population = Population()
    population.individuals.extend(args)
    return population


def population_equal(first: Population, second: Population) -> bool:
    return first.individuals == second.individuals
