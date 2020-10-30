import pytest
import numpy as np

from model.elements.chromosome import make_chromosome, chromosome_equal


@pytest.fixture()
def lists():
    first_array = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    second_array = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    third_array = np.array([1, 0, 1, 0, 1, 0, 1, 0])
    ones_array = np.array([1 for i in range(8)])
    zeros_array = np.array([0 for i in range(8)])
    return first_array, second_array, third_array, ones_array, zeros_array


@pytest.fixture()
def chromosomes(lists):
    first_array, second_array, third_array, ones_array, zeros_array = lists
    first = make_chromosome(first_array)
    second = make_chromosome(second_array)
    third = make_chromosome(third_array)
    ones = make_chromosome(ones_array)
    zeros = make_chromosome(zeros_array)
    return first, second, third, ones, zeros


class TestChromosome:
    @pytest.fixture(autouse=True)
    def _init_chromosomes(self, chromosomes):
        self.first, self.second, self.third, self.ones, self.zeros = chromosomes

    def test_make_chromosome_length(self, lists):
        assert all(len(getattr(self, x)) == 8 for x in ("first", "second", "third", "ones", "zeros"))

    def test_make_chromosome_content(self, lists):
        first_array, second_array, third_array, ones_array, zeros_array = lists
        assert np.array_equal(self.first.genes, first_array)
        assert np.array_equal(self.second.genes, second_array)
        assert np.array_equal(self.third.genes, third_array)
        assert np.array_equal(self.ones.genes, ones_array)
        assert np.array_equal(self.zeros.genes, zeros_array)

    def test_chromosome_equal_the_same_chromosome(self):
        assert chromosome_equal(self.first, self.first)

    def test_chromosome_equal_different_chromosomes(self):
        assert not chromosome_equal(self.first, self.second)

    def test_logical_not(self):
        assert chromosome_equal(self.ones.logical_not(), self.zeros)
        assert chromosome_equal(self.zeros.logical_not(), self.ones)

    def test_partial_logical_not_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_not([]), self.first)

    def test_partial_logical_not(self):
        assert chromosome_equal(self.first.partial_logical_not([0, 2, 5, 7]), self.third)
        assert chromosome_equal(self.second.partial_logical_not([1, 3, 4, 6]), self.third)

    def test_logical_or_same_input(self):
        assert chromosome_equal(self.second.logical_or(self.second), self.second)

    def test_logical_or(self):
        assert chromosome_equal(self.first.logical_or(self.second), self.ones)

    def test_logical_or_symmetric(self):
        assert chromosome_equal(self.second.logical_or(self.third), self.third.logical_or(self.second))

    def test_partial_logical_or_empty_index_array(self):
        assert chromosome_equal(self.second.partial_logical_or(self.second, []), self.second)

    def test_partial_logical_or(self):
        assert chromosome_equal(self.first.partial_logical_or(self.second, [0, 2, 4, 6]).partial_logical_not([5, 7]),
                                self.third)
        assert chromosome_equal(self.second.partial_logical_or(self.third, [1, 3, 4, 6]).partial_logical_not([5, 7]),
                                self.ones)

    def test_partial_logical_or_asymmetric(self):
        assert not chromosome_equal(self.second.partial_logical_or(self.third, [0, 2, 4, 6]),
                                    self.third.partial_logical_or(self.second, [0, 2, 4, 6]))

    def test_logical_and_same_input(self):
        assert chromosome_equal(self.first.logical_and(self.first), self.first)

    def test_logical_and(self):
        assert chromosome_equal(self.first.logical_and(self.second), self.zeros)
        assert chromosome_equal(self.ones.logical_and(self.first), self.first)
        assert chromosome_equal(self.zeros.logical_and(self.first), self.zeros)

    def test_logical_and_symmetric(self):
        assert chromosome_equal(self.second.logical_and(self.third), self.third.logical_and(self.second))

    def test_partial_logical_and_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_and(self.zeros, []), self.first)

    def test_partial_logical_and(self):
        assert chromosome_equal(self.first.partial_logical_and(self.second, [4, 5, 6, 7]), self.zeros)
        assert chromosome_equal(self.second.partial_logical_and(self.first, [4, 5, 6, 7]), self.second)

    def test_partial_logical_and_asymmetric(self):
        assert not chromosome_equal(self.second.partial_logical_and(self.third, [1, 3, 5, 7]),
                                    self.third.partial_logical_and(self.second, [1, 3, 5, 7]))
        
    def test_combine_with_make_chromosome(self):
        def function(c1, c2):
            return make_chromosome(c1.genes + c2.genes)
        assert chromosome_equal(self.first.combine(self.second, function), make_chromosome(self.first.genes + self.second.genes))

    def test_combine_with_logical_function(self):
        def function(c1, c2):
            return c1.logical_and(c2)
        assert chromosome_equal(self.first.combine(self.second, function), self.zeros)

    def test_combine_with_nested_logical_function(self):
        def function(c1, c2):
            return c1.logical_and(c2).logical_not()
        assert chromosome_equal(self.first.combine(self.second, function), self.ones)

    def test_complete_to(self):
        larger_chromosome = make_chromosome(np.array([1 for i in range(1000)]))
        completed_chromosome = self.second.complete_to(larger_chromosome)
        assert len(completed_chromosome) == len(larger_chromosome)
        assert np.array_equal(completed_chromosome[:len(self.second)], self.second.genes)
        assert np.array_equal(completed_chromosome[len(self.second):],
                              larger_chromosome[:len(completed_chromosome) - len(self.second)])

    def test_complete_to_random(self):
        larger_chromosome = make_chromosome(np.array([0 for i in range(1000)]))
        completed_chromosome = self.second.complete_to_random(larger_chromosome)
        assert len(completed_chromosome) == len(larger_chromosome)
        assert all(i < 2 for i in completed_chromosome)
        assert not np.array_equal(completed_chromosome[len(self.second):],
                                  larger_chromosome[:len(completed_chromosome) - len(self.second)])
