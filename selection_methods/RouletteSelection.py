import math

import numpy as np

from selection_methods.SelectionMethod import SelectionMethod


class RouletteSelection(SelectionMethod):
    def select_next_generation(self, population, population_evaluate):
        super().select_next_generation(population, population_evaluate)
        raise NotImplementedError
