import pytest
from copy import deepcopy

from model.elements.population import population_equal
from model.algorithms.mutation import *
from .fixtures import *


mutations = [EdgeMutation(), Inversion()]
all_mutations = [PointMutation(), UniformMutation()] + mutations


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


def test_check_required_parameters_uniform_mutation():
    mutation = UniformMutation()
    mutation["chromosomes"] = ["a", "b"]
    mutation["probability"] = 0.1
    mutation["min"] = 2
    mutation["max"] = 12
    mutation["precision"] = 2
    mutation["fill"] = 16
    mutation.check_required_parameters()
    del mutation["chromosomes"]
    del mutation["probability"]
    del mutation["min"]
    del mutation["max"]
    del mutation["precision"]
    del mutation["fill"]


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
        self.uniform_mutation = UniformMutation()

        self.one_point_mutation["points"] = 1
        self.two_point_mutation["points"] = 2

        self.uniform_mutation["min"] = 2
        self.uniform_mutation["max"] = 12
        self.uniform_mutation["precision"] = 2
        self.uniform_mutation["fill"] = 16

        for x in ("one_point_mutation", "two_point_mutation", "edge_mutation", "inversion", "uniform_mutation"):
            getattr(self, x)["chromosomes"] = self.chromosomes
            getattr(self, x)["probability"] = 1

    @pytest.mark.parametrize("mutation",
                             ["one_point_mutation", "two_point_mutation", "edge_mutation", "inversion", "uniform_mutation"])
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
        assert_mutations(mutated_population, self.population, self.chromosomes, lambda actual: actual > 0)

    def test_uniform_mutation(self):
        mutated_population = self.inversion.invoke(deepcopy(self.population))
        assert_mutations(mutated_population, self.population, self.chromosomes, lambda actual: actual > 0)


def assert_mutations(mutated_population: Population, original_population: Population, chromosomes, assertion):
    for chromosome in chromosomes:
        for mutated, original in zip(mutated_population.individuals, original_population.individuals):
            actual = 0
            for x, y in zip(mutated[chromosome].genes, original[chromosome].genes):
                if x != y:
                    actual += 1
            assert assertion(actual)
