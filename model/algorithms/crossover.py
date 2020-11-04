from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Crossover(GeneticOperator, ABC):
    pass


class PointCrossover(Crossover):
    def invoke(self, population: Population) -> Population:
        pass


class HomogenousCrossover(Crossover):
    def invoke(self, population: Population) -> Population:
        pass
