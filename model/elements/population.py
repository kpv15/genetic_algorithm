from functools import reduce
from typing import List, Tuple

from model.elements import Individual, make_random_individual


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

    def get_fitness_list_and_sum(self, fitness_function) -> Tuple[List, float]:
        fitness_list, result = [], 0
        for individual in self.individuals:
            fitness_list.append(fitness_function(individual))
            result += fitness_function(individual)
        return fitness_list, result

    def get_fitness_list_with_indexes(self, fitness_function) -> List:
        fitness_list = []
        for i, individual in enumerate(self.individuals):
            fitness_list.append((fitness_function(individual), i))
        return fitness_list


def make_population(*args) -> Population:
    population = Population()
    population.individuals.extend(args)
    return population


def make_random_population(population_size: int, chromosome_size: int, chromosome_names: List[str]):
    population = Population()
    for i in range(population_size):
        population.append(make_random_individual(chromosome_size, chromosome_names))
    return population


def population_equal(first: Population, second: Population) -> bool:
    return first.individuals == second.individuals
