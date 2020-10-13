import random
from typing import Tuple

from genetic_operators.crossover_methods.CrossingMethod import CrossingMethod

# todo one/two/three point crossing
from population_model.PopulationMember import PopulationMember


class OnePointCrossing(CrossingMethod):

    def cross_pair(self, generation_members_pair: Tuple[PopulationMember, PopulationMember]):
        x, y = generation_members_pair
        chromosome_length = x.chromosomes_number * x.genes_number
        cut_point = random.randrange(chromosome_length)

        for i in range(chromosome_length):
            if i < cut_point:
                self.__swap_genes(x, y, i)
                pass
            else:
                break

        return x, y

    @staticmethod
    def __swap_genes(a, b, i):
        tmp = a.chromosome_array[i]
        a.chromosome_array[i] = b.chromosome_array[i]
        b.chromosome_array[i] = tmp
