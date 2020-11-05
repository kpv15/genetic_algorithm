from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Crossover(GeneticOperator, ABC):
    pass


class PointCrossover(Crossover):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class HomogenousCrossover(Crossover):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass
