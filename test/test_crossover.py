import pytest

from model.elements import make_chromosome, individual_equal
from model.elements.population import population_equal, make_population
from model.algorithms.crossover import *
from model.algorithms.fitness_functions import *
from .fixtures import *

all_crossovers = [PointCrossover(), UniformCrossover()]


@pytest.mark.parametrize("crossover", all_crossovers)
def test_get_and_set_item(crossover):
    crossover["int"] = 123
    crossover["function"] = lambda x: x ** 2
    assert crossover["int"] == 123
    assert crossover["function"](2) == 4


def test_check_required_parameters_uniform_crossover():
    crossover = UniformCrossover()
    crossover["chromosomes"] = ["a", "b"]
    crossover["probability"] = 0.1
    crossover.check_required_parameters()
    del crossover["chromosomes"]
    del crossover["probability"]


def test_check_required_parameters_point_crossover():
    crossover = PointCrossover()
    crossover["chromosomes"] = ["a", "b"]
    crossover["probability"] = 0.1
    crossover["points"] = 10
    crossover.check_required_parameters()
    del crossover["chromosomes"]
    del crossover["probability"]
    del crossover["points"]


@pytest.mark.parametrize("crossover", all_crossovers)
def test_check_required_parameters_not_present(crossover):
    with pytest.raises(KeyError):
        crossover.check_required_parameters()


class TestCrossover:
    @pytest.fixture(autouse=True)
    def _init_crossovers(self, small_population_and_individuals):
        self.population, self.first, self.second, self.ones = small_population_and_individuals

        self.chromosomes = ["x"]
        self.probability = 0.5
        self.one_point_crossover, self.two_point_crossover, self.three_point_crossover = PointCrossover(), PointCrossover(), PointCrossover()
        self.uniform_crossover = UniformCrossover()

        self.one_point_crossover["points"] = 1
        self.two_point_crossover["points"] = 2
        self.three_point_crossover["points"] = 3

        for x in ("one_point_crossover", "two_point_crossover", "three_point_crossover", "uniform_crossover"):
            getattr(self, x)["chromosomes"] = self.chromosomes
            getattr(self, x)["probability"] = self.probability

    @pytest.mark.parametrize("crossover",
                             ["one_point_crossover", "two_point_crossover", "three_point_crossover", "uniform_crossover"])
    def test_crossover(self, crossover):
        crossed_population = getattr(self, crossover).invoke(self.population)
        for individual in crossed_population:
            assert not individual_equal(individual, self.ones)
            assert not individual_equal(individual, self.ones)
