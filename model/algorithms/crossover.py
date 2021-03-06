from abc import ABC, abstractmethod
from random import sample, randrange, uniform

from model.algorithms.genetic_operator import GeneticOperator
from model.elements import Population, Individual, Chromosome, make_real_chromosome


class Crossover(GeneticOperator, ABC):
    def check_required_parameters(self):
        if "chromosomes" not in self:
            raise KeyError("Crossover::'chromosomes' is missing")
        if "probability" not in self:
            raise KeyError("Crossover::'probability' is missing")

    def invoke(self, population: Population) -> Population:
        crossed_population = Population()
        for index, first in enumerate(population.individuals):
            if not self._cross_with_candidate(population, crossed_population, first, index):
                crossed_population.extend(*self._cross(first, population.individuals[-1]))
        return crossed_population

    def _cross_with_candidate(self, population, crossed_population, first, index):
        for second in population.individuals[index:]:
            if uniform(0, 1) <= self["probability"]:
                crossed_population.extend(*self._cross(first, second))
                return True
        return False

    @abstractmethod
    def _cross(self, first: Individual, second: Individual):
        pass


class PointCrossover(Crossover):
    def check_required_parameters(self):
        if "points" not in self:
            raise KeyError("PointCrossover::'points' is missing")
        super().check_required_parameters()

    def _cross(self, first: Individual, second: Individual):
        result1, result2 = Individual(), Individual()

        for chromosome in self["chromosomes"]:
            length = len(first[chromosome])
            crossover_points = sorted(sample(range(0, length), self["points"]))
            if length - 1 not in crossover_points:
                crossover_points.append(length - 1)

            result1[chromosome] = Chromosome(length)
            result2[chromosome] = Chromosome(length)

            last_crossover_point = 0
            for i, crossover_point in enumerate(crossover_points):
                if i % 2 == 0:
                    result1[chromosome][last_crossover_point:crossover_point] = first[chromosome][last_crossover_point:crossover_point]
                    result2[chromosome][last_crossover_point:crossover_point] = second[chromosome][last_crossover_point:crossover_point]
                else:
                    result1[chromosome][last_crossover_point:crossover_point] = second[chromosome][last_crossover_point:crossover_point]
                    result2[chromosome][last_crossover_point:crossover_point] = first[chromosome][last_crossover_point:crossover_point]

        return result1, result2


class UniformCrossover(Crossover):
    def _cross(self, first: Individual, second: Individual):
        result = Individual()

        for chromosome in self["chromosomes"]:
            result[chromosome] = Chromosome(len(first[chromosome]))
            for i in range(0, len(first[chromosome])):
                if randrange(1, 11) <= 5:
                    result[chromosome][i] = first[chromosome][i]
                else:
                    result[chromosome][i] = second[chromosome][i]

        return result,


class RealCrossover(Crossover, ABC):
    def check_required_parameters(self):
        if "k_selection_function" not in self:
            raise KeyError("RealCrossover::'k_selection_function' is missing")
        if "precisions" not in self:
            raise KeyError("RealCrossover::'precisions' is missing")
        if "fills" not in self:
            raise KeyError("RealCrossover::'fills' is missing")
        super().check_required_parameters()


class ArithmeticCrossover(RealCrossover):
    def _cross(self, first: Individual, second: Individual):
        k = self["k_selection_function"]()
        result1, result2 = Individual(), Individual()

        for chromosome in self["chromosomes"]:
            precision = self["precisions"][chromosome]
            fill = self["fills"][chromosome]

            first_decoded = first[chromosome].decode(precision)
            second_decoded = second[chromosome].decode(precision)
            result1[chromosome] = make_real_chromosome(k * first_decoded + (1 - k) * second_decoded, precision, fill)
            result2[chromosome] = make_real_chromosome((1 - k) * first_decoded + k * second_decoded, precision, fill)

        return result1, result2


class HeuristicCrossover(RealCrossover):
    def _cross(self, first: Individual, second: Individual):
        for chromosome in self["chromosomes"]:
            precision = self["precisions"][chromosome]
            if first[chromosome].decode(precision) > second[chromosome].decode(precision):
                return first, second

        k = self["k_selection_function"]()
        result = Individual()

        for chromosome in self["chromosomes"]:
            precision = self["precisions"][chromosome]
            fill = self["fills"][chromosome]

            first_decoded = first[chromosome].decode(precision)
            second_decoded = second[chromosome].decode(precision)
            result[chromosome] = make_real_chromosome(k * (second_decoded - first_decoded) + first_decoded, precision, fill)

        return result,
