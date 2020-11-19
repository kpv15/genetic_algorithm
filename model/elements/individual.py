import numpy as np
from typing import List, Dict

from model.elements import chromosome_equal, make_random_chromosome


class Individual:
    __slots__ = "chromosomes"

    def __init__(self):
        self.chromosomes = {}

    def __getitem__(self, item):
        return self.chromosomes[item]

    def __setitem__(self, key, value):
        self.chromosomes[key] = value

    def __len__(self):
        return len(self.chromosomes)

    def extend(self, *args):
        for i in args:
            self.chromosomes = dict(self.chromosomes, **i.chromosomes)

    def remove(self, chromosomes_names: List[str]):
        for i in chromosomes_names:
            if i in self.chromosomes:
                del self.chromosomes[i]

    def combine(self, individual, function):
        return function(self, individual)

    def decode(self, precision: Dict):
        result = {}
        for key, value in self.chromosomes.items():
            result[key] = value.decode(precision[key])
        return result


def make_individual(*args) -> Individual:
    individual = Individual()
    for i in args:
        individual.chromosomes = dict(individual.chromosomes, **i)
    return individual


def make_random_individual(chromosome_size: int, chromosome_names: List[str]) -> Individual:
    individual = Individual()
    for name in chromosome_names:
        individual[name] = make_random_chromosome(chromosome_size)
    return individual


def individual_equal(first: Individual, second: Individual) -> bool:
    if len(first) != len(second):
        return False

    for v1, v2 in zip(first.chromosomes.values(), second.chromosomes.values()):
        if not chromosome_equal(v1, v2):
            return False

    return True
