import pytest
from functools import partial

from model.algorithms.fitness_functions import *
from .fixtures import *


class TestFitnessFunctions:
    @pytest.fixture(autouse=True)
    def _init_individuals(self, individuals):
        self.first, self.second, self.third, self.ones, self.zeros = individuals

    def test_count_nonzero_fitness_function(self):
        assert count_nonzero_fitness_function(self.ones) == 8
        assert count_nonzero_fitness_function(self.zeros) == 0
        assert count_nonzero_fitness_function(self.first) == 12

    def test_ackley_function_minimum_fitness_function(self):
        precisions = {"x": 3, "y": 3, "z": 3, "ones": 3, "zeros": 3}
        fitness_function = partial(ackley_function_minimum_fitness_funtion, precisions)

        for individual in ("first", "second", "third", "ones"):
            assert fitness_function(getattr(self, individual)) < fitness_function(self.zeros)

    def test_ackley_function_maximum_fitness_function(self):
        precisions = {"x": 3, "y": 3, "z": 3, "ones": 3, "zeros": 3}
        fitness_function = partial(ackley_function_maximum_fitness_funtion, precisions)

        for individual in ("first", "second", "third", "ones"):
            assert fitness_function(getattr(self, individual)) > fitness_function(self.zeros)
