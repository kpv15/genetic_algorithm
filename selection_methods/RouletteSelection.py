import math

import numpy as np

from population_model.Population import Population
from selection_methods.SelectionMethod import SelectionMethod


class RouletteSelection(SelectionMethod):
    def select_next_generation(self, population: Population, population_evaluate: np.ndarray):
        elite_indexes = super().save_elite(population, population_evaluate)
        for i, index in enumerate(elite_indexes):
            population.add_next_generation_member(population.return_population_member(index))

        temp_eval = np.array(population_evaluate)
        worst_member_evaluate = population_evaluate.min()
        if worst_member_evaluate <= 0:
            temp_eval += math.fabs(worst_member_evaluate) + 1  # todo check this 1

        if self.search_minimum:
            temp_eval = np.reciprocal(temp_eval)

        temp_eval = np.cumsum(temp_eval)

        for i in range(len(elite_indexes), population.population_size):
            r = np.random.random() * temp_eval[-1]
            for j in range(population.population_size):
                if temp_eval[j] > r:
                    survivor = population.return_population_member(j)
                    break
            population.add_next_generation_member(survivor)
        population.change_of_generations()

    def __init__(self, part_of_guarded, search_minimum=False):
        super().__init__(part_of_guarded, search_minimum)
