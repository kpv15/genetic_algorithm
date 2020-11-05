from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Mutation(GeneticOperator, ABC):
    pass


class PointMutation(Mutation):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class EdgeMutation(Mutation):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class Inversion(Mutation):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass
