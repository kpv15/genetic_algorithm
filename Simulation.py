import numpy as np

from genetic_operators.InversionMethod import InversionMethod
from genetic_operators.crossover_methods import CrossingMethod
from genetic_operators.mutation_methods import MutationMethod
from population_model.Population import Population
from selection_methods.SelectionMethod import SelectionMethod
from evaluate_functions.EvaluateFunction import EvaluateFunction


class Simulation:
    population = None  # type: Population
    generations_max_number = None
    selection_method = None  # type: SelectionMethod
    crossing_method = None  # type: CrossingMethod
    mutation_method = None  # type: MutationMethod
    evaluation_function = None  # type: EvaluateFunction
    inversion_method = None  # type: InversionMethod
    file_output = None

    def __init__(self, population, generations_max_number, selection_method, crossover_method, mutation_method,
                 evaluation_function, inversion_method=None, file_output=None):
        self.population = population
        self.generations_max_number = generations_max_number
        self.selection_method = selection_method
        self.crossing_method = crossover_method
        self.mutation_method = mutation_method
        self.evaluation_function = evaluation_function
        self.inversion_method = inversion_method
        self.file_output = file_output

    def simulate(self):
        for i in range(self.generations_max_number):
            population_evaluate = self.__evaluate_population()
            if self.file_output is not None:
                self.file_output.write(self.population)
                self.file_output.write(population_evaluate)
            self.selection_method.select_next_generation(self.population, population_evaluate)
            self.crossing_method.cross_population(self.population)
            self.mutation_method.mutate_population(self.population)
            if self.inversion_method is not None:
                self.population = self.inversion_method.make_inversions_in_population(self.population)

    def __evaluate_population(self):
        population_evaluate_tmp = []
        for population_member in self.population:
            population_evaluate_tmp.append(self.evaluation_function.evaluate(population_member.decode_member()))
        population_evaluate = np.asarray(population_evaluate_tmp)
        return population_evaluate
