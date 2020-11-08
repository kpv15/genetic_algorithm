import pytest

from model.elements.population import population_equal
from model.algorithms.selection import *
from model.algorithms.fitness_functions import *
from .fixtures import *

selections = [TheBestOfSelection(), RouletteSelection(), EliteStrategy()]
selections_all = selections + [TournamentSelection()]


@pytest.mark.parametrize("selection", selections_all)
def test_get_and_set_item(selection):
    selection["int"] = 123
    selection["function"] = lambda x: x ** 2
    assert selection["int"] == 123
    assert selection["function"](2) == 4


@pytest.mark.parametrize("selection", selections)
def test_check_required_parameters_present(selection):
    selection["count"] = 5
    selection["fitness_function"] = lambda x: x ** 2
    selection.check_required_parameters()
    del selection["count"]
    del selection["fitness_function"]


def test_check_required_parameters_tournament_selection():
    selection = TournamentSelection()
    selection["count"] = 5
    selection["fitness_function"] = lambda x: x ** 2
    selection["tournament_size"] = 10
    selection.check_required_parameters()


@pytest.mark.parametrize("selection", selections_all)
def test_check_required_parameters_not_present(selection):
    with pytest.raises(KeyError):
        selection.check_required_parameters()


class TestSelection:
    @pytest.fixture(autouse=True)
    def _init_selection(self, big_populations, individuals):
        self.first, self.second, self.third, self.ones, self.zeros = big_populations
        self.first_individual, self.second_individual, self.third_individual, self.ones_individual, self.zeros_individual = individuals
        self.the_best_of_selection = TheBestOfSelection()
        self.roulette_selection = RouletteSelection()
        self.tournament_selection = TournamentSelection()
        self.elite_strategy = EliteStrategy()

        self.count = 10
        self.fitness_function = count_nonzero_fitness_function
        self.tournament_size = 5

        for selection in ("the_best_of_selection", "roulette_selection", "tournament_selection", "elite_strategy"):
            getattr(self, selection)["count"] = self.count
            getattr(self, selection)["fitness_function"] = self.fitness_function
        self.tournament_selection["tournament_size"] = self.tournament_size

        for selection in ("the_best_of_selection", "roulette_selection", "tournament_selection", "elite_strategy"):
            getattr(self, selection).check_required_parameters()

    def test_the_best_of_selection_invoke(self):
        assert population_equal(self.the_best_of_selection.invoke(self.first),
                                make_population(*[self.first_individual for _ in range(self.count)]))
        assert population_equal(self.the_best_of_selection.invoke(self.second),
                                make_population(*[self.second_individual for _ in range(self.count)]))
