import math

import numpy as np

from population_model.Population import Population
from selection_methods.SelectionMethod import SelectionMethod


class RouletteSelection(SelectionMethod):
    def select_next_generation(self, population: Population, population_evaluate: np.ndarray):
        elite_indexes = super().__save_elite(population, population_evaluate)
        new_population = np.empty([population.population_size, population.genes_number * population.chromosomes_number])
        for i, index in enumerate(elite_indexes):
            new_population[i] = population[index]

        temp_eval = np.array(population_evaluate)
        worst_member_evaluate = population_evaluate.min()
        if worst_member_evaluate <= 0:
            temp_eval += math.fabs(worst_member_evaluate) + 1  # todo check this 1
        temp_eval = np.cumsum(temp_eval)

        new_population = Population()
        for i in range(len(elite_indexes), population.population_size):
            r = np.random.random() * temp_eval[-1]
            for j in enumerate(population.population_size):
                if temp_eval[j] > r:
                    survivor = population.return_population_member(j)
                    break
            new_population[i] = survivor

        return new_population

    def __init__(self, part_of_guarded, search_minimum=False):
        super().__init__(part_of_guarded, search_minimum)
