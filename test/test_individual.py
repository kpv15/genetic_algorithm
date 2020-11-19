import pytest

from copy import copy
from functools import partial

from model.elements.individual import *
from .fixtures import *


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

    @pytest.mark.parametrize("precisions,results", [
        ({"x": 0, "y": 0, "z": 0, "ones": 0, "zeros": 0},
            [{"x": 15, "y": 240, "z": 170}, {"x": 15, "y": 240}, {"z": 170}, {"ones": 255}, {"zeros": 0}]),
        ({"x": 2, "y": 3, "z": 0, "ones": 4, "zeros": 6},
            [{"x": 3.75, "y": 30, "z": 170}, {"x": 3.75, "y": 30}, {"z": 170}, {"ones": 15.9375}, {"zeros": 0}]),
        ({"x": 4, "y": 0, "z": 8, "ones": 8, "zeros": 8},
            [{"x": 0.9375, "y": 240, "z": 0.6640625}, {"x": 0.9375, "y": 240}, {"z": 0.6640625}, {"ones": 0.99609375}, {"zeros": 0}])])
    def test_decode(self, precisions, results):
        assert self.first.decode(precisions) == results[0]
        assert self.second.decode(precisions) == results[1]
        assert self.third.decode(precisions) == results[2]
        assert self.ones.decode(precisions) == results[3]
        assert self.zeros.decode(precisions) == results[4]
