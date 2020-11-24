from model.algorithms import Selection, Crossover, Mutation, Inversion, EliteStrategy
from model.elements import Population


class Simulation:
    population: Population = None
    generations_max_number = None
    selection_method: Selection = None
    crossing_method: Crossover = None
    mutation_method: Mutation = None
    evaluation_function = None
    elite_function: EliteStrategy = None
    inversion_method: Inversion = None
    value_history = []
    minimum = False

    def __init__(self, population, generations_max_number, selection_method, crossover_method, mutation_method,
                 evaluation_function, elite_function, inversion_method, minimum):
        self.population = population
        self.generations_max_number = generations_max_number
        self.selection_method = selection_method
        self.crossing_method = crossover_method
        self.mutation_method = mutation_method
        self.evaluation_function = evaluation_function
        self.elite_function = elite_function
        self.inversion_method = inversion_method
        self.value_history = []
        self.minimum = minimum

    def simulate(self):
        for i in range(self.generations_max_number):
            self.elite_function.invoke(self.population)
            elite = self.elite_function["elite"]
            self.population = self.selection_method.invoke(self.population)
            self.population = self.crossing_method.invoke(self.population)
            self.population = self.mutation_method.invoke(self.population)
            self.population = self.inversion_method.invoke(self.population)
            self.population.extend(*elite)
            self.__save_generation_to_file()
        self.population.individuals

        self.elite_function["count"] = 1
        self.elite_function.invoke(self.population)
        elite = self.elite_function["elite"]

        result_params = elite[0].decode(self.evaluation_function.args[0])
        result_value = self.evaluation_function(elite[0])
        if self.minimum:
            result_value = -result_value
        print("result =", result_params, 'val = ', result_value)
        return result_params, result_value, self.value_history

    def __save_generation_to_file(self):
        (fitness_list, result) = self.population.get_fitness_list_and_sum(self.evaluation_function)
        if self.minimum:
            fitness_list = [-x for x in fitness_list]
        # print(fitness_list)
        self.value_history.append(fitness_list)
