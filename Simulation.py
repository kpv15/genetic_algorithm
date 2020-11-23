from evaluate_functions.EvaluateFunction import EvaluateFunction
from model.algorithms import Selection, Crossover, Mutation, Inversion, EliteStrategy
from model.elements import Population


class Simulation:
    population: Population = None
    generations_max_number = None
    selection_method: Selection = None
    crossing_method: Crossover = None
    mutation_method: Mutation = None
    evaluation_function: EvaluateFunction = None
    elite_function: EliteStrategy = None
    inversion_method: Inversion = None
    file_output = None

    def __init__(self, population, generations_max_number, selection_method, crossover_method, mutation_method,
                 evaluation_function, elite_function, inversion_method, file_output=None):
        self.population = population
        self.generations_max_number = generations_max_number
        self.selection_method = selection_method
        self.crossing_method = crossover_method
        self.mutation_method = mutation_method
        self.evaluation_function = evaluation_function
        self.elite_function = elite_function
        self.inversion_method = inversion_method
        self.file_output = file_output

    def simulate(self):
        for i in range(self.generations_max_number):
            self.elite_function.invoke(self.population)
            elite = self.elite_function["elite"]
            self.population = self.selection_method.invoke(self.population)
            self.population = self.crossing_method.invoke(self.population)
            self.population = self.mutation_method.invoke(self.population)
            self.population = self.inversion_method.invoke(self.population)
            self.population.extend(*elite)
            if self.file_output is not None:
                self.__save_generation_to_file()
        self.population.individuals

    def __save_generation_to_file(self):
        (fitness_list, result) = self.population.get_fitness_list_and_sum(self.evaluation_function)
        print(fitness_list)
