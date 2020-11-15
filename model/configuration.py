from model.algorithms import *


class Configuration:
    __slots__ = ("selection", "crossover", "mutation", "elite_strategy", "inversion")

    def __init__(self, selection_method: Selection, crossover_method: Crossover, mutation_method: Mutation):
        self.selection = selection_method
        self.crossover = crossover_method
        self.mutation = mutation_method
        self.elite_strategy = EliteStrategy()
        self.inversion = Inversion()
