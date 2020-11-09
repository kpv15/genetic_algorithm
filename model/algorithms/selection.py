from abc import ABC, abstractmethod
from random import uniform, sample
from typing import List, Tuple

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population, Individual, make_population


class Selection(GeneticOperator, ABC):
    def check_required_parameters(self):
        if "count" not in self:
            raise KeyError("Selection::'count' is missing")
        if "fitness_function" not in self:
            raise KeyError("Selection::'fitness_function' is missing")

    def invoke(self, population: Population) -> Population:
        preprocessed_list = self._preprocess_fitness_list(population)
        subpopulation = []
        for i in range(self["count"]):
            subpopulation.append(self._select(population, preprocessed_list))
        return make_population(*subpopulation)

    @abstractmethod
    def _preprocess_fitness_list(self, population: Population) -> List[Tuple[float, int]]:
        pass

    @abstractmethod
    def _select(self, population: Population, preprocessed_list: List[Tuple[float, int]]) -> Individual:
        pass


class TheBestOfSelection(Selection):
    def _preprocess_fitness_list(self, population: Population) -> List[Tuple[float, int]]:
        self["actual"] = 0
        return sorted(population.get_fitness_list_with_indexes(self["fitness_function"]), key=lambda x: x[0], reverse=True)

    def _select(self, population: Population, preprocessed_list: List[Tuple[float, int]]) -> Individual:
        self["actual"] += 1
        return population[preprocessed_list[self["actual"] - 1][1]]


class RouletteSelection(Selection):
    def _preprocess_fitness_list(self, population: Population) -> List[Tuple[float, int]]:
        fitness_list, fitness_of_all = population.get_fitness_list_and_sum(self["fitness_function"])
        preprocessed_list = []
        for i, fitness in enumerate(fitness_list):
            preprocessed_list.append((fitness / fitness_of_all, i))
        return sorted(preprocessed_list, key=lambda x: x[0])

    def _select(self, population: Population, preprocessed_list: List[Tuple[float, int]]) -> Individual:
        random_number = uniform(0, 1)
        for fitness, index in preprocessed_list:
            if random_number < fitness:
                return population[index]
        return population[preprocessed_list[-1][1]]


class TournamentSelection(Selection):
    def check_required_parameters(self):
        if "tournament_size" not in self:
            raise KeyError("TournamentSelection::'tournament_size' is missing")
        return super().check_required_parameters()

    def _preprocess_fitness_list(self, population: Population) -> List[Tuple[float, int]]:
        return population.get_fitness_list_with_indexes(self["fitness_function"])

    def _select(self, population: Population, preprocessed_list: List[Tuple[float, int]]) -> Individual:
        tournament = sample(range(0, len(population)), self["tournament_size"])
        max_fitness, max_index = preprocessed_list[tournament[0]][0], preprocessed_list[tournament[0]][1]
        for i in tournament:
            if preprocessed_list[i][0] > max_fitness:
                max_fitness, max_index = preprocessed_list[i][0], i
        return population[max_index]


class EliteStrategy(Selection):
    def _preprocess_fitness_list(self, population: Population) -> List[Tuple[float, int]]:
        self["elite"] = []
        self["actual"] = 0
        return sorted(population.get_fitness_list_with_indexes(self["fitness_function"]), key=lambda x: x[0], reverse=True)

    def _select(self, population: Population, preprocessed_list: List[Tuple[float, int]]) -> Individual:
        self["actual"] += 1
        self["elite"].append(population[preprocessed_list[self["actual"] - 1][1]])
        return population[preprocessed_list[self["actual"] - 1][1]]

    def get_elite_as_population(self) -> Population:
        return make_population(*self["elite"])
