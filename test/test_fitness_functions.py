import pytest

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
