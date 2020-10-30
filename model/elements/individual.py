from typing import Dict, List

from model.elements.chromosome import chromosome_equal, Chromosome


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


def make_individual(*args) -> Individual:
    individual = Individual()
    for i in args:
        individual.chromosomes = dict(individual.chromosomes, **i)
    return individual


def individual_equal(first: Individual, second: Individual) -> bool:
    if len(first) != len(second):
        return False

    for v1, v2 in zip(first.chromosomes.values(), second.chromosomes.values()):
        if not chromosome_equal(v1, v2):
            return False

    return True
