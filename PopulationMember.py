import numpy as np


class PopulationMember:
    chromosome_array = None
    chromosomes_number = None
    minimum_value = None
    maximum_value = None
    dx = None
    genes_number = None

    def __init__(self, chromosome_array, chromosomes_number, minimum_value, maximum_value, dx, genes_number):
        self.chromosome_array = chromosome_array
        self.chromosomes_number = chromosomes_number
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.dx = dx
        self.genes_number = genes_number

    def decode_member(self):
        decode_individual = np.zeros(self.chromosomes_number)
        for i in range(self.genes_number):
            tmp = 1
            for j in range(self.genes_number * i, self.genes_number * i - 1, -1):
                decode_individual[i] += tmp * self.chromosome_array[j]
                tmp *= 2
            decode_individual[i] = decode_individual[i] * self.dx + self.minimum_value
        return decode_individual
