from abc import ABC

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population


class Selection(GeneticOperator, ABC):
    pass


class TheBestOfSelection(Selection):
    def invoke(self, population: Population) -> Population:
        pass


class RouletteSelection(Selection):
    def invoke(self, population: Population) -> Population:
        pass


class TournamentSelection(Selection):
    def invoke(self, population: Population) -> Population:
        pass


class EliteStrategy(Selection):
    def invoke(self, population: Population) -> Population:
        pass
