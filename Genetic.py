from GUI.GUI import GUI
from Simulation import Simulation
from evaluate_functions.TestFunction import TestFunction
from model.algorithms import PointCrossover, UniformCrossover, PointMutation, EdgeMutation, TheBestOfSelection, \
    TournamentSelection, RouletteSelection, Inversion

from model.elements import make_random_population, calculate_the_number_of_genes


class Genetic:
    selection_methods = {
        "The best of selection": (TheBestOfSelection,),
        "Roulette selection": (RouletteSelection,),
        "Tournament Selection": (TournamentSelection,)
    }
    crossing_methods = {
        "One point crossing": (PointCrossover, ("points", 1)),
        "Two point crossing": (PointCrossover, ("points", 2)),
        "Three point crossing": (PointCrossover, ("points", 3)),
        "Uniform crossing": (UniformCrossover,)
    }
    mutation_methods = {
        "One point mutation": (PointMutation, ("points", 1)),
        "Two point mutation": (PointMutation, ("points", 2)),
        "Three point mutation": (PointMutation, ("points", 3)),
        "Edge mutation": (EdgeMutation,)
    }

    def __init__(self):
        self.gui = GUI(self, list(self.selection_methods.keys()), list(self.mutation_methods.keys()),
                       list(self.crossing_methods.keys()))

    def run(self):
        self.gui.show()

    @staticmethod
    def create_strategy(config):
        strategy = config[0]()
        for dict_element in config[1:]:
            strategy[dict_element[0]] = dict_element[1]
        return strategy

    def start_work(self, minimum_value, maximum_value, dx_value, population_size, generations_number,
                   elite_strategy_value, inversion_probability, crossing_probability, mutation_probability,
                   selection_method_name, tournament_size, mutation_method_name, crossing_method_name):
        file = open("result.txt", "w")

        function = TestFunction()
        population = make_random_population(population_size,
                                            calculate_the_number_of_genes(minimum_value, maximum_value, dx_value),
                                            function.getParameterNames())

        selection_strategy = self.create_strategy(self.selection_methods[selection_method_name])
        selection_strategy["count"] = population_size
        selection_strategy["fitness_function"] = function.evaluate
        selection_strategy["tournament_size"] = tournament_size
        selection_strategy.check_required_parameters()

        mutation_strategy = self.create_strategy(self.mutation_methods[mutation_method_name])
        mutation_strategy["chromosomes"] = function.getParameterNumber()
        mutation_strategy["probability"] = mutation_probability
        mutation_strategy.check_required_parameters()

        crossing_strategy = self.create_strategy(self.crossing_methods[crossing_method_name])
        crossing_strategy["chromosomes"] = function.getParameterNumber()
        crossing_strategy["probability"] = crossing_probability
        crossing_strategy.check_required_parameters()

        inversion_strategy = Inversion()
        inversion_strategy["chromosomes"] = function.getParameterNumber()
        inversion_strategy["probability"] = inversion_probability
        inversion_strategy.check_required_parameters()

        simulation = Simulation(population, generations_number, selection_strategy, crossing_strategy,
                                mutation_strategy, function, inversion_strategy, file)
        simulation.simulate()

        file.close()


if __name__ == "__main__":
    genetic = Genetic()
    genetic.run()
