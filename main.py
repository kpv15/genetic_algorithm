from Simulation import Simulation
from evaluate_functions.TestFunction import TestFunction
from genetic_operators.crossover_methods.PointCrossing import PointCrossing
from population_model.Population import Population
from selection_methods.RouletteSelection import RouletteSelection
from genetic_operators.mutation_methods.PointMutation import PointMutation

function = TestFunction()
population = Population(8, -10, 10, function.getValuesNumber(), 2)
simulation = Simulation(population, 200, RouletteSelection(0.1, search_minimum=True), PointCrossing(), PointMutation(),
                        function)
simulation.simulate()
