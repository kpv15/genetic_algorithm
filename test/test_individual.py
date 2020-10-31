import pytest

from copy import copy
from functools import partial

from model.elements.individual import *
from .test_chromosome import chromosomes, lists


@pytest.fixture
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
    first = make_individual(first_dict)
    second = make_individual(second_dict)
    third = make_individual(third_dict)
    ones = make_individual(ones_dict)
    zeros = make_individual(zeros_dict)
    return first, second, third, ones, zeros


class TestIndividual:
    @pytest.fixture(autouse=True)
    def _init_individuals(self, individuals):
        self.first, self.second, self.third, self.ones, self.zeros = individuals

    def test_make_individual_length(self, dicts):
        first, second, third, ones, zeros = dicts
        assert all(len(getattr(self, x)) == len(y)
                   for x, y in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros)))

    def test_make_individual_content(self, dicts):
        first, second, third, ones, zeros = dicts
        assert all(getattr(self, x).chromosomes == y
                   for x, y in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros)))

    def test_individual_equal_the_same_individual(self):
        assert individual_equal(self.first, self.first)

    def test_individual_equal_different_individual_different_length(self):
        assert not individual_equal(self.first, self.second)

    def test_individual_equal_different_individual_the_same_length(self):
        assert not individual_equal(self.ones, self.zeros)

    def test_individual_setitem(self, chromosomes):
        _, _, third_chromosome, _, _ = chromosomes
        second = copy(self.second)
        second["z"] = third_chromosome
        assert individual_equal(second, self.first)

    def test_extend_one(self):
        individual = Individual()
        individual.extend(self.ones)
        assert individual_equal(individual, self.ones)

    def test_extend_many(self):
        individual = Individual()
        individual.extend(self.first)
        assert individual_equal(individual, self.first)

    def test_extend_multiple(self, dicts):
        first, second, third, _, _ = dicts
        individual = Individual()
        individual.extend(make_individual(first), make_individual(second), make_individual(third))
        assert individual_equal(individual, self.first)

    def test_remove_missing_chromosome(self):
        first = copy(self.first)
        first.remove(["missing"])
        assert individual_equal(first, self.first)

    def test_remove_present_chromosome(self):
        first = copy(self.first)
        first.remove(["z"])
        assert individual_equal(first, self.second)

    def test_combine_with_make_individual(self):
        def function(i1, i2):
            return make_individual(dict(i1.chromosomes, **i2.chromosomes))

        assert individual_equal(self.first, self.second.combine(self.third, function))

    def test_combine_with_logical_function_and_make_individual(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2)

        def function_individual(i1, i2):
            return make_individual({"zeros": i1["x"].combine(i2["y"], function_chromosomes)})

        assert individual_equal(self.first.combine(self.second, function_individual), self.zeros)

    def test_combine_with_partial(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2).logical_not()

        def function_individual(function, i1, i2):
            return make_individual({"ones": i1["x"].combine(i2["y"], function)})

        assert individual_equal(self.first.combine(self.second, partial(function_individual, function_chromosomes)), self.ones)

    def test_make_random_individual_size(self):
        individual = make_random_individual(32, ["x", "y", "z"])
        assert len(individual) == 3
        assert all(len(val) == 32 for val in individual.chromosomes.values())

    def test_make_random_chromosome_randomness(self):
        individual1 = make_random_individual(200, ["x", "y", "z"])
        individual2 = make_random_individual(200, ["x", "y", "z"])
        assert not individual_equal(individual1, individual2)
