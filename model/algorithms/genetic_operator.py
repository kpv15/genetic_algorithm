from abc import ABC, abstractmethod

from model.elements import Population


class GeneticOperator(ABC):
    __slots__ = "parameters"

    def __init__(self):
        self.parameters = {}

    def __getitem__(self, item):
        return self.parameters[item]

    def __setitem__(self, key, value):
        self.parameters[key] = value

    def invoke(self, population: Population) -> Population:
        self._check_required_parameters()
        return self._invoke(population)

    @abstractmethod
    def _check_required_parameters(self):
        pass

    @abstractmethod
    def _invoke(self, population: Population) -> Population:
        pass
