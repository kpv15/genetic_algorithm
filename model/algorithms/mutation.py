from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Mutation(GeneticOperator, ABC):
    pass


class PointMutation(Mutation):
    def invoke(self, population: Population) -> Population:
        pass

    def check_required_parameters(self):
        pass


class EdgeMutation(Mutation):
    def invoke(self, population: Population) -> Population:
        pass

    def check_required_parameters(self):
        pass


class Inversion(Mutation):
    def invoke(self, population: Population) -> Population:
        pass

    def check_required_parameters(self):
        pass
