from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Selection(GeneticOperator, ABC):
    pass


class TheBestOfSelection(Selection):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class RouletteSelection(Selection):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class TournamentSelection(Selection):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass


class EliteStrategy(Selection):
    def _invoke(self, population: Population) -> Population:
        pass

    def _check_required_parameters(self):
        pass
