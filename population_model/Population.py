import math

import numpy as np

from population_model.PopulationMember import PopulationMember
from Exceptions import OutOfRangeException, PopulationIsFullException


class Population:
    # from user
    chromosomes_number = None
    minimum_value = None
    maximum_value = None
    requested_dx = None
    population_size = None
    # calculated
    dx = None
    genes_number = None
    population_array = None
    next_population_array = None
    next_population_member_count = None
    # for iterator
    iterator_value = None

    def __init__(self, population_size, minimum_value, maximum_value, chromosomes_number, requested_dx):
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.chromosomes_number = chromosomes_number
        self.requested_dx = requested_dx
        self.population_size = population_size
        self.__calculate_the_number_of_genes_and_real_dx()
        self.__generate_population()

    def __calculate_the_number_of_genes_and_real_dx(self):
        interval = math.fabs(self.maximum_value - self.minimum_value)
        combination_number = math.ceil(interval / self.requested_dx)

        genes_number = 0
        x = combination_number
        while x >= 1:
            x = x / 2
            genes_number += 1
        real_combination_number = 2 ** genes_number

        self.genes_number = genes_number
        self.dx = interval / (real_combination_number - 1)

    def __generate_population(self):
        self.population_array = np.random.randint(2, size=(
            self.population_size, self.genes_number * self.chromosomes_number))

    def return_population_member(self, i):
        if i < 0 or i >= self.population_size:
            raise OutOfRangeException()
        return PopulationMember(self.population_array[i], self.chromosomes_number, self.minimum_value,
                                self.maximum_value,
                                self.dx, self.genes_number)

    def add_next_generation_member(self, population_member: PopulationMember):
        if self.next_population_array is None:
            self.next_population_array = np.empty([self.population_size, self.genes_number * self.chromosomes_number], dtype=int)
            self.next_population_member_count = 0
        elif self.next_population_member_count >= self.population_size:
            raise PopulationIsFullException
        self.next_population_array[self.next_population_member_count] = population_member.chromosome_array
        self.next_population_member_count += 1

    def change_of_generations(self):
        self.population_array = self.next_population_array
        self.next_population_array = None

    def __iter__(self):
        self.iterator_value = 0
        return self

    def __next__(self):
        if self.iterator_value >= self.population_size:
            raise StopIteration
        else:
            i = self.iterator_value
            self.iterator_value += 1
            return self.return_population_member(i)

    def __str__(self):
        return str(self.population_array)
