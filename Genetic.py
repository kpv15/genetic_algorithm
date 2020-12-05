from functools import partial

from GUI.GUI import GUI
from PlotGenerator import PlotGenerator
from Simulation import Simulation
from model.algorithms import PointCrossover, UniformCrossover, PointMutation, EdgeMutation, TheBestOfSelection, \
    TournamentSelection, RouletteSelection, Inversion, ackley_function_minimum_fitness_funtion, EliteStrategy, \
    ackley_function_maximum_fitness_funtion

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

    def start_work(self, x_value, digits_count, population_size, generations_number,
                   elite_strategy_value, inversion_probability, crossing_probability, mutation_probability,
                   selection_method_name, tournament_size, mutation_method_name, crossing_method_name, minimum):
        file = open("result.txt", "w")

        elite_strategy_count = round(population_size * elite_strategy_value)
        variables_names = ['x', 'y']
        population = make_random_population(population_size,
                                            calculate_the_number_of_genes(x_value),
                                            variables_names)

        precisions = {"x": digits_count, "y": digits_count}

        if minimum:
            fitness_function = partial(ackley_function_minimum_fitness_funtion, precisions)
        else:
            fitness_function = partial(ackley_function_maximum_fitness_funtion, precisions)

        selection_strategy = self.create_strategy(self.selection_methods[selection_method_name])
        selection_strategy["count"] = round(population_size - elite_strategy_count)
        selection_strategy["fitness_function"] = fitness_function
        selection_strategy["tournament_size"] = tournament_size
        selection_strategy.check_required_parameters()

        mutation_strategy = self.create_strategy(self.mutation_methods[mutation_method_name])
        mutation_strategy["chromosomes"] = variables_names
        mutation_strategy["probability"] = mutation_probability
        mutation_strategy.check_required_parameters()

        crossing_strategy = self.create_strategy(self.crossing_methods[crossing_method_name])
        crossing_strategy["chromosomes"] = variables_names
        crossing_strategy["probability"] = crossing_probability
        crossing_strategy.check_required_parameters()

        inversion_strategy = Inversion()
        inversion_strategy["chromosomes"] = variables_names
        inversion_strategy["probability"] = inversion_probability
        inversion_strategy.check_required_parameters()

        elite_strategy = EliteStrategy()
        elite_strategy["count"] = elite_strategy_count
        elite_strategy["fitness_function"] = fitness_function
        elite_strategy["tournament_size"] = tournament_size
        elite_strategy.check_required_parameters()

        simulation = Simulation(population, generations_number, selection_strategy, crossing_strategy,
                                mutation_strategy, fitness_function, elite_strategy, inversion_strategy, minimum)
        result_params, result_value, value_history = simulation.simulate()
        self.gui.show_result(result_params, result_value)
        PlotGenerator().generate(value_history, minimum)
        for epoch in value_history:
            file.write(str(epoch) + '\n')
        file.close()


if __name__ == "__main__":
    genetic = Genetic()
    genetic.run()
