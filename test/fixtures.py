import pytest
import numpy as np

from model.elements import make_chromosome, make_individual, make_population, Individual


@pytest.fixture
def lists():
    first_list = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    second_list = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    third_list = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    ones_list = np.array([1 for _ in range(8)])
    zeros_list = np.array([0 for _ in range(8)])
    return first_list, second_list, third_list, ones_list, zeros_list


@pytest.fixture
def chromosomes(lists):
    first_array, second_array, third_array, ones_array, zeros_array = lists
    first = make_chromosome(first_array)
    second = make_chromosome(second_array)
    third = make_chromosome(third_array)
    ones = make_chromosome(ones_array)
    zeros = make_chromosome(zeros_array)
    return first, second, third, ones, zeros


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


@pytest.fixture
def big_populations(individuals):
    first, second, third, ones, zeros = individuals

    def _make_population(individual):
        return make_population(*([individual for _ in range(25)] + [ones for _ in range(25)] + [zeros for _ in range(25)]))

    first_population = _make_population(first)
    second_population = _make_population(second)
    third_population = _make_population(third)
    ones_population = make_population(*([ones for _ in range(50)] + [first for _ in range(25)]))
    zeros_population = make_population(*([zeros for _ in range(50)] + [first for _ in range(25)]))

    return first_population, second_population, third_population, ones_population, zeros_population

@pytest.fixture
def small_population_and_individuals():
    first, second, ones = Individual(), Individual(), Individual()
    first["x"] = make_chromosome(np.asarray([1, 0, 1, 0, 1, 0, 1, 0]))
    second["x"] = make_chromosome(np.asarray([0, 1, 0, 1, 0, 1, 0, 0]))
    ones["x"] = make_chromosome(np.asarray([1, 1, 1, 1, 1, 1, 1, 1]))
    population = make_population(first, second)
    return population, first, second, ones
