from typing import Dict, List

from model.elements.chromosome import chromosome_equal


class Individual:
    __slots__ = "chromosomes"

    def __init__(self):
        self.chromosomes = {}

    def __getitem__(self, item):
        return self.chromosomes[item]

    def __setitem__(self, key, value):
        self.chromosomes[key] = value

    def size(self):
        return len(self.chromosomes)

    def remove(self, chromosomes_names: List[str]):
        for i in chromosomes_names:
            del self.chromosomes[i]

    def combine(self, individual, function):
        return function(self, individual)


def make_individual(dictionary: Dict) -> Individual:
    individual = Individual()
    individual.chromosomes = dictionary
    return individual


def individual_equal(individual1: Individual, individual2: Individual) -> bool:
    if individual1.size() != individual2.size():
        return False

    for v1, v2 in zip(individual1.chromosomes.values(), individual2.chromosomes.values()):
        if not chromosome_equal(v1, v2):
            return False
    return True
