import pytest
from copy import copy
from functools import partial

from model.elements.individual import make_individual, individual_equal
from model.elements.population import *
from .test_individual import individuals, chromosomes, lists, dicts


@pytest.fixture
def individuals_lists(individuals):
    first, second, third, ones, zeros = individuals
    first_list = [first, second]
    second_list = [second, third]
    third_list = [third, ones, zeros]
    ones_list = [ones]
    zeros_list = [zeros]
    return first_list, second_list, third_list, ones_list, zeros_list


@pytest.fixture
def populations(individuals_lists):
    first_list, second_list, third_list, ones_list, zeros_list = individuals_lists
    first = make_population(*first_list)
    second = make_population(*second_list)
    third = make_population(*third_list)
    ones = make_population(*ones_list)
    zeros = make_population(*zeros_list)
    return first, second, third, ones, zeros


class TestPopulation:
    @pytest.fixture(autouse=True)
    def _init_populations(self, populations):
        self.first, self.second, self.third, self.ones, self.zeros = populations

    def test_make_population_length(self, individuals_lists):
        first, second, third, ones, zeros = individuals_lists
        assert all(len(getattr(self, x)) == len(y)
                   for x, y in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros)))

    def test_make_population_content(self, individuals_lists):
        first, second, third, ones, zeros = individuals_lists
        assert all(individual_equal(x, y)
                   for a, b in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros))
                   for x, y in zip(getattr(self, a).individuals, b))

    def test_population_equal_the_same_population(self):
        assert population_equal(self.first, self.first)

    def test_population_equal_different_population(self):
        assert not population_equal(self.first, self.second)

    def test_population_setitem(self, individuals):
        first, second, _, _, _ = individuals
        population = Population()
        population[:2] = first, second
        assert population_equal(population, self.first)

    def test_all_indexes(self):
        assert self.first.all_indexes() == [0, 1]
        assert self.zeros.all_indexes() == [0]

    def test_append(self, individuals):
        _, _, _, ones, _ = individuals
        population = Population()
        population.append(ones)
        assert population_equal(population, self.ones)

    def test_extend(self, individuals):
        first, second, _, _, _ = individuals
        population = Population()
        population.extend(first, second)
        assert population_equal(population, self.first)

    def test_remove_missing_individual(self):
        first = copy(self.first)
        first.remove([3, 15])
        assert population_equal(first, self.first)

    def test_remove_present_chromosome(self):
        third = copy(self.third)
        third.remove([0, 2])
        assert population_equal(third, self.ones)

    def test_reduce_with_make_individual(self):
        def function(i1, i2):
            return make_individual(dict(i1.chromosomes, **i2.chromosomes))

        population = copy(self.second)
        population.append(self.second.reduce(self.second.all_indexes(), function))
        individual = Individual()
        individual.extend(*self.second.individuals)
        assert individual_equal(population[-1], individual)

    def test_reduce_with_logical_function_and_make_individual(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2)

        def function_individual(i1, i2):
            return make_individual({"zeros": i1["x"].combine(i2["y"], function_chromosomes)})

        population = copy(self.first)
        population.append(self.first.reduce([0, 1], function_individual))
        individual = Individual()
        individual.extend(*self.zeros.individuals)
        assert individual_equal(population[-1], individual)

    def test_reduce_with_partial(self):
        def function_chromosomes(c1, c2):
            return c1.logical_and(c2)

        def function_individual(function, i1, i2):
            return make_individual({"zeros": i1["x"].combine(i2["y"], function)})

        population = copy(self.first)
        population.append(self.first.reduce([0, 1], partial(function_individual, function_chromosomes)))
        individual = Individual()
        individual.extend(*self.zeros.individuals)
        assert individual_equal(population[-1], individual)

    def test_make_random_population_size(self):
        population = make_random_population(10, 32, ["x", "y", "z"])
        assert len(population) == 10
        assert all(len(val) == 3 for val in population.individuals)
        assert all(len(val) == 32 for individual in population.individuals for val in individual.chromosomes.values())

    def test_make_random_population_randomness(self):
        population1 = make_random_population(10, 200, ["x", "y", "z"])
        population2 = make_random_population(10, 200, ["x", "y", "z"])
        assert not population_equal(population1, population2)
