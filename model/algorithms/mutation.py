from abc import ABC, abstractmethod
from random import uniform, sample, randrange

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population, Chromosome, make_real_chromosome


class Mutation(GeneticOperator, ABC):
    def check_required_parameters(self):
        if "chromosomes" not in self:
            raise KeyError("Mutation::'chromosomes' is missing")
        if "probability" not in self:
            raise KeyError("Mutation::'probability' is missing")

    def invoke(self, population: Population) -> Population:
        for chromosome in self["chromosomes"]:
            for individual in population.individuals:
                if uniform(0, 1) <= self["probability"]:
                    self._mutate(individual[chromosome])
        return population

    @abstractmethod
    def _mutate(self, chromosome: Chromosome):
        pass


class PointMutation(Mutation):
    def check_required_parameters(self):
        if "points" not in self:
            raise KeyError("PointMutation::'points' is missing")
        super().check_required_parameters()

    def _mutate(self, chromosome: Chromosome):
        indexes = sample(range(0, len(chromosome)), self["points"])
        chromosome.partial_logical_not_inplace(indexes)


class EdgeMutation(Mutation):
    def _mutate(self, chromosome: Chromosome):
        chromosome.partial_logical_not_inplace([len(chromosome)-1])


class Inversion(Mutation):
    def _mutate(self, chromosome: Chromosome):
        indexes = sample(range(0, len(chromosome) + 1), 2)
        chromosome.partial_logical_not_inplace(list(range(indexes[0], indexes[1]) if indexes[0] < indexes[1]
                                                    else range(indexes[1], indexes[0])))


class UniformMutation(Mutation):
    def check_required_parameters(self):
        if "min" not in self:
            raise KeyError("UniformMutation::'min' is missing")
        if "max" not in self:
            raise KeyError("UniformMutation::'max' is missing")
        if "precision" not in self:
            raise KeyError("UniformMutation::'precision' is missing")
        if "fill" not in self:
            raise KeyError("UniformMutation::'fill' is missing")
        super().check_required_parameters()

    def _mutate(self, chromosome: Chromosome):
        chromosome.replace(make_real_chromosome(randrange(self["min"], self["max"]), self["precision"], self["fill"]))
