import numpy as np


class PopulationMember:
    chromosome_array = None
    chromosomes_number = None
    minimum_value = None
    maximum_value = None
    dx = None
    genes_number = None
    max_phenotype_value = None

    def __init__(self, chromosome_array, chromosomes_number, minimum_value, maximum_value, dx, genes_number):
        self.chromosome_array = chromosome_array
        self.chromosomes_number = chromosomes_number
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.dx = dx
        self.genes_number = genes_number
        self.max_phenotype_value = 2 ** genes_number

    def decode_member(self):
        phenotype = np.zeros(self.chromosomes_number)
        member_values = np.zeros(self.chromosomes_number)
        for i in range(self.chromosomes_number):
            tmp = 1
            for j in range(self.genes_number * i - 1, self.genes_number * (i - 1) - 1, -1):
                phenotype[i] += tmp * self.chromosome_array[j]
                tmp *= 2
            member_values[i] = self.minimum_value + phenotype[i] / self.max_phenotype_value * (
                        self.maximum_value - self.minimum_value)
        return member_values
