from copy import copy
from functools import partial

import pytest

from model.elements.chromosome import *
from model.elements.individual import *

from .TestChromosome import chromosomes, lists


@pytest.fixture()
def dicts(chromosomes):
    first, second, third, ones, zeros = chromosomes
    first_dict = {"x": first, "y": second, "z": third}
    second_dict = {"x": first, "y": second}
    third_dict = {"z": third}
    ones_dict = {"ones": ones}
    zeros_dict = {"zeros": zeros}
    return first_dict, second_dict, third_dict, ones_dict, zeros_dict


@pytest.fixture
def individuals(dicts):
    first_dict, second_dict, third_dict, ones_dict, zeros_dict = dicts
    first_individual = make_individual(first_dict)
    second_individual = make_individual(second_dict)
    third_individual = make_individual(third_dict)
    ones_individual = make_individual(ones_dict)
    zeros_individual = make_individual(zeros_dict)
    return first_individual, second_individual, third_individual, ones_individual, zeros_individual


def test_make_individual(individuals, dicts):
    first, second, third, ones, zeros = individuals
    first_dict, second_dict, third_dict, ones_dict, zeros_dict = dicts
    assert first.chromosomes == first_dict
    assert second.chromosomes == second_dict
    assert third.chromosomes == third_dict
    assert zeros.chromosomes == zeros_dict
    assert ones.chromosomes == ones_dict


class TestIndividual:

    @pytest.fixture(autouse=True)
    def _init_individuals(self, individuals):
        self.first, self.second, self.third, self.ones, self.zeros = individuals

    def test_individual_equal(self):
        assert individual_equal(self.first, self.first)
        assert not individual_equal(self.first, self.second)

    def test_remove(self):
        first = copy(self.first)
        first.remove(["z"])
        assert individual_equal(first, self.second)

    def test_combine_simple(self):
        def function(i1, i2):
            return make_individual(dict(i1.chromosomes, **i2.chromosomes))
        assert individual_equal(self.first, self.second.combine(self.third, function))

    def test_combine_normal(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2)

        def function_individual(i1, i2):
            return make_individual({"zeros": i1["x"].combine(i2["y"], function_chromosomes)})

        assert individual_equal(self.first.combine(self.second, function_individual), self.zeros)

    def test_combine_hard(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2).logical_not()

        def function_individual(function, i1, i2):
            return make_individual({"ones": i1["x"].combine(i2["y"], function)})

        assert individual_equal(self.first.combine(self.second, partial(function_individual, function_chromosomes)), self.ones)
