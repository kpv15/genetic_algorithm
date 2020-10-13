from Simulation import Simulation
from evaluate_functions.TestFunction import TestFunction
from genetic_operators.crossover_methods.OnePointCrossing import OnePointCrossing
from population_model.Population import Population
from selection_methods.RouletteSelection import RouletteSelection
from genetic_operators.mutation_methods.PointMutation import PointMutation

file = open("result.txt", "w")

function = TestFunction()
population = Population(10, -5, 10, function.getValuesNumber(), 0.1)
simulation = Simulation(population, 100, RouletteSelection(0.1, search_minimum=True), OnePointCrossing(0.8),
                        PointMutation(), function, file_output=file)
simulation.simulate()

file.close()
