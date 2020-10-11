import numpy as np

from crossover_methods.CrossoverMethod import CrossoverMethod
from mutation_methods.MutationMethod import MutationMethod
from population_model.Population import Population
from selection_methods.SelectionMethod import SelectionMethod
from evaluate_functions.EvaluateFunction import EvaluateFunction


class Simulation:
    population = None  # type: Population
    generations_max_number = None
    selection_method = None  # type: SelectionMethod
    crossover_method = None  # type: CrossoverMethod
    mutation_method = None  # type: MutationMethod
    evaluation_function = None  # type: EvaluateFunction

    def __init__(self, population, generations_max_number, selection_method, crossover_method, mutation_method,
                 evaluation_function):
        self.population = population
        self.generations_max_number = generations_max_number
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.evaluation_function = evaluation_function

    def simulate(self):
        for i in range(self.generations_max_number):
            population_evaluate = self.evaluate_population()
            self.population = self.selection_method.select_next_generation(self.population, population_evaluate)
            self.population = self.crossover_method.crossover_population(self.population)
            self.population = self.mutation_method.mutate_population(self.population)

    def evaluate_population(self):
        population_evaluate_tmp = []
        for population_member in self.population:
            population_evaluate_tmp.append(self.evaluation_function.evaluate(population_member.decode_member()))
        population_evaluate = np.asarray(population_evaluate_tmp)
        return population_evaluate
