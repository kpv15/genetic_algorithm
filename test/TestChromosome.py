import pytest
import numpy as np

from model.Chromosome import make_chromosome, chromosome_equal


@pytest.fixture()
def lists():
    first_array = [0, 0, 0, 0, 1, 1, 1, 1]
    second_array = [1, 1, 1, 1, 0, 0, 0, 0]
    third_array = [1, 0, 1, 0, 1, 0, 1, 0]
    ones_array = [1 for i in range(8)]
    zeros_array = [0 for i in range(8)]
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

    def test_make_chromosome(self, lists):
        first_array, second_array, third_array, ones_array, zeros_array = lists
        assert all(getattr(self, x).genes.size == 8 for x in ("first", "second", "third", "ones", "zeros"))
        assert np.array_equal(self.first.genes, first_array)
        assert np.array_equal(self.second.genes, second_array)
        assert np.array_equal(self.third.genes, third_array)
        assert np.array_equal(self.ones.genes, ones_array)
        assert np.array_equal(self.zeros.genes, zeros_array)

    def test_logical_not(self):
        assert chromosome_equal(self.ones.logical_not(), self.zeros)
        assert chromosome_equal(self.zeros.logical_not(), self.ones)

    def test_partial_logical_not_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_not([]), self.first)
        assert chromosome_equal(self.second.partial_logical_not([]), self.second)

    def test_partial_logical_not(self):
        assert chromosome_equal(self.first.partial_logical_not([0, 2, 5, 7]), self.third)
        assert chromosome_equal(self.second.partial_logical_not([1, 3, 4, 6]), self.third)

    def test_logical_or_same_input(self):
        assert chromosome_equal(self.first.logical_or(self.first), self.first)
        assert chromosome_equal(self.second.logical_or(self.second), self.second)

    def test_logical_or(self):
        assert chromosome_equal(self.first.logical_or(self.second), self.ones)
        assert chromosome_equal(self.second.logical_or(self.first), self.ones)

    def test_partial_logical_or_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_or(self.second, []), self.first)
        assert chromosome_equal(self.second.partial_logical_or(self.second, []), self.second)

    def test_partial_logical_or(self):
        assert chromosome_equal(self.first.partial_logical_or(self.second, [0, 2, 4, 6]).partial_logical_not([5, 7]),
                                self.third)
        assert chromosome_equal(self.second.partial_logical_or(self.third, [1, 3, 4, 6]).partial_logical_not([5, 7]),
                                self.ones)

    def test_logical_and_same_input(self):
        assert chromosome_equal(self.first.logical_and(self.first), self.first)
        assert chromosome_equal(self.second.logical_and(self.second), self.second)

    def test_logical_and(self):
        assert chromosome_equal(self.first.logical_and(self.second), self.zeros)
        assert chromosome_equal(self.ones.logical_and(self.first), self.first)
        assert chromosome_equal(self.zeros.logical_and(self.first), self.zeros)

    def test_partial_logical_and_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_and(self.zeros, []), self.first)
        assert chromosome_equal(self.second.partial_logical_and(self.ones, []), self.second)

    def test_partial_logical_and(self):
        assert chromosome_equal(self.first.partial_logical_and(self.second, [4, 5, 6, 7]), self.zeros)
        assert chromosome_equal(self.second.partial_logical_and(self.first, [4, 5, 6, 7]), self.second)

    def test_complete_to(self):
        larger_chromosome = make_chromosome([1 for i in range(1000)])
        completed_chromosome = self.second.complete_to(larger_chromosome)
        assert completed_chromosome.size() == larger_chromosome.size()
        assert np.array_equal(completed_chromosome[:self.second.size()], self.second.genes)
        assert np.array_equal(completed_chromosome[self.second.size():],
                              larger_chromosome[:completed_chromosome.size() - self.second.size()])

    def test_complete_to_random(self):
        larger_chromosome = make_chromosome([0 for i in range(1000)])
        completed_chromosome = self.second.complete_to_random(larger_chromosome)
        assert completed_chromosome.size() == larger_chromosome.size()
        assert all(i < 2 for i in completed_chromosome)
        assert not np.array_equal(completed_chromosome[self.second.size():],
                                  larger_chromosome[:completed_chromosome.size() - self.second.size()])
