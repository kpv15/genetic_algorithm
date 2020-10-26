from GUI.GUI import GUI
from Simulation import Simulation
from evaluate_functions.TestFunction import TestFunction
from genetic_operators.crossing_methods.OnePointCrossing import OnePointCrossing
from population_model.Population import Population
from selection_methods.RouletteSelection import RouletteSelection
from genetic_operators.mutation_methods.PointMutation import PointMutation


class Genetic:
    crossing_methods = {"One point crossing": OnePointCrossing}
    mutation_methods = {"Point mutation": PointMutation}
    selection_methods = {"Roulette selection": RouletteSelection}

    def __init__(self):
        self.gui = GUI(self, list(self.selection_methods.keys()), list(self.mutation_methods.keys()),
                       list(self.crossing_methods.keys()))

    def run(self):
        self.gui.show()

    def start_work(self, minimum_value, maximum_value, dx_value, population_size, generations_number,
                   elite_strategy_value, immersion_operator_value, crossing_probability, mutation_probability,
                   selection_method_name, mutation_method_name, crossing_method_name):
        file = open("result.txt", "w")

        selection_class = self.selection_methods[selection_method_name]
        mutation_class = self.mutation_methods[mutation_method_name]
        crossing_class = self.crossing_methods[crossing_method_name]

        function = TestFunction()
        population = Population(population_size, minimum_value, maximum_value, function.getValuesNumber(), dx_value)
        simulation = Simulation(population, generations_number,
                                selection_class(elite_strategy_value, search_minimum=True),
                                crossing_class(crossing_probability), mutation_class(mutation_probability), function,
                                file_output=file)
        simulation.simulate()

        file.close()


if __name__ == "__main__":
    genetic = Genetic()
    genetic.run()
