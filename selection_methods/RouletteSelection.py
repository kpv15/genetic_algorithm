import math

import numpy as np

from selection_methods.SelectionMethod import SelectionMethod


class RouletteSelection(SelectionMethod):
    def select_next_generation(self, population, population_evaluate):
        super().select_next_generation()
        raise NotImplementedError
    # temp_evaluation = np.array(population_evaluate)
    # y, x = population.shape
    # min = np.amin(temp_evaluation)
    # if (min <= 0):
    #     temp_evaluation += math.fabs(min) + 1
    # temp_evaluation = np.cumsum(temp_evaluation)
    # new_population = np.empty([y, x], dtype=int)
    # for i in range(y):
    #     r = np.random.random() * temp_evaluation[-1]
    #     for j in range(y):
    #         if temp_evaluation[j] > r:
    #             survivor = population[j]
    #             break
    #     new_population[i] = survivor
    #
    # return new_population
