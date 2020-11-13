import pytest
from copy import deepcopy

from model.elements import make_chromosome, individual_equal
from model.elements.population import population_equal, make_population
from model.algorithms.mutation import *
from model.algorithms.fitness_functions import *
from .fixtures import *


mutations = [EdgeMutation(), Inversion()]
all_mutations = [PointMutation()] + mutations


@pytest.mark.parametrize("mutation", all_mutations)
def test_get_and_set_item(mutation):
    mutation["int"] = 123
    mutation["function"] = lambda x: x ** 2
    assert mutation["int"] == 123
    assert mutation["function"](2) == 4


@pytest.mark.parametrize("mutation", mutations)
def test_check_required_parameters_mutations(mutation):
    mutation["chromosomes"] = ["a", "b"]
    mutation["probability"] = 0.1
    mutation.check_required_parameters()
    del mutation["chromosomes"]
    del mutation["probability"]


def test_check_required_parameters_point_mutation():
    mutation = PointMutation()
    mutation["chromosomes"] = ["a", "b"]
    mutation["probability"] = 0.1
    mutation["points"] = 10
    mutation.check_required_parameters()
    del mutation["chromosomes"]
    del mutation["probability"]
    del mutation["points"]


@pytest.mark.parametrize("mutation", all_mutations)
def test_check_required_parameters_not_present(mutation):
    with pytest.raises(KeyError):
        mutation.check_required_parameters()


class TestMutation:
    @pytest.fixture(autouse=True)
    def _init_mutations(self, small_population_and_individuals):
        self.population, self.first, self.second, self.ones = small_population_and_individuals
        self.chromosomes = ["x"]

        self.one_point_mutation, self.two_point_mutation = PointMutation(), PointMutation()
        self.edge_mutation = EdgeMutation()
        self.inversion = Inversion()

        self.one_point_mutation["points"] = 1
        self.two_point_mutation["points"] = 2

        for x in ("one_point_mutation", "two_point_mutation", "edge_mutation", "inversion"):
            getattr(self, x)["chromosomes"] = self.chromosomes
            getattr(self, x)["probability"] = 1

    @pytest.mark.parametrize("mutation",
                             ["one_point_mutation", "two_point_mutation", "edge_mutation", "inversion"])
    def test_mutations_exists(self, mutation):
        mutated_population = getattr(self, mutation).invoke(deepcopy(self.population))
        assert not population_equal(mutated_population, self.population)

    @pytest.mark.parametrize("mutation,count",
                             [("one_point_mutation", 1), ("two_point_mutation", 2)])
    def test_point_mutations(self, mutation, count):
        mutated_population = getattr(self, mutation).invoke(deepcopy(self.population))
        assert_mutations(mutated_population, self.population, self.chromosomes, lambda actual: actual == count)

    def test_edge_mutations(self):
        mutated_population = self.edge_mutation.invoke(deepcopy(self.population))
        assert_mutations(mutated_population, self.population, self.chromosomes, lambda actual: actual == 1)
        assert mutated_population[0][self.chromosomes[0]][-1] != self.population[0][self.chromosomes[0]][-1]
        assert mutated_population[1][self.chromosomes[0]][-1] != self.population[1][self.chromosomes[0]][-1]

    def test_inversion(self):
        mutated_population = self.inversion.invoke(deepcopy(self.population))
        assert_mutations(mutated_population, self.population, self.chromosomes, lambda actual: actual > 2)


def assert_mutations(mutated_population: Population, original_population: Population, chromosomes, assertion):
    for chromosome in chromosomes:
        for mutated, original in zip(mutated_population.individuals, original_population.individuals):
            actual = 0
            for x, y in zip(mutated[chromosome].genes, original[chromosome].genes):
                if x != y:
                    actual += 1
            assert assertion(actual)
