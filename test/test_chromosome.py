import pytest
from copy import copy

from model.elements.chromosome import *
from .fixtures import *


@pytest.mark.parametrize("number,precision,fill,result", [
    (0, 0, 2, [0, 0]), (0.5, 1, 2, [0, 1]), (1, 0, 0, [1]),
    (1.5, 1, 4, [0, 0, 1, 1]), (1.5, 0, 0, [1]),
    (50.75, 2, 10, [0, 0, 1, 1, 0, 0, 1, 0, 1, 1])])
def test_make_real_chromosome(number, precision, fill, result):
    chromosome = make_real_chromosome(number, precision, fill)
    assert np.array_equal(chromosome.genes, result)


class TestChromosome:
    @pytest.fixture(autouse=True)
    def _init_chromosomes(self, chromosomes):
        self.first, self.second, self.third, self.ones, self.zeros = chromosomes

    def test_make_chromosome_length(self, lists):
        first, second, third, ones, zeros = lists
        assert all(len(getattr(self, x)) == len(y)
                   for x, y in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros)))

    def test_make_chromosome_content(self, lists):
        first, second, third, ones, zeros = lists
        assert all(np.array_equal(getattr(self, x).genes, y)
                   for x, y in zip(("first", "second", "third", "ones", "zeros"), (first, second, third, ones, zeros)))

    def test_chromosome_equal_the_same_chromosome(self):
        assert chromosome_equal(self.first, self.first)

    def test_chromosome_equal_different_chromosomes(self):
        assert not chromosome_equal(self.first, self.second)

    def test_chromosome_setitem(self):
        first = copy(self.first)
        first[:4] = True
        assert chromosome_equal(first, self.ones)

    def test_logical_not(self):
        assert chromosome_equal(self.ones.logical_not(), self.zeros)
        assert chromosome_equal(self.zeros.logical_not(), self.ones)

    def test_partial_logical_not_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_not([]), self.first)

    def test_partial_logical_not(self):
        assert chromosome_equal(self.first.partial_logical_not([0, 2, 5, 7]), self.third)
        assert chromosome_equal(self.second.partial_logical_not([1, 3, 4, 6]), self.third)

    def test_partial_logical_not_inplace_empty_index_array(self):
        first = copy(self.first)
        first.partial_logical_not_inplace([])
        assert chromosome_equal(first, self.first)

    def test_partial_logical_not_inplace(self):
        first = copy(self.first)
        first.partial_logical_not_inplace([0, 2, 5, 7])
        second = copy(self.second)
        second.partial_logical_not_inplace([1, 3, 4, 6])

        assert chromosome_equal(first, self.third)
        assert chromosome_equal(second, self.third)

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

    def test_logical_xor_same_input(self):
        assert chromosome_equal(self.first.logical_xor(self.first), self.zeros)

    def test_logical_xor(self):
        assert chromosome_equal(self.first.logical_xor(self.second), self.ones)
        assert chromosome_equal(self.zeros.logical_xor(self.ones), self.ones)

    def test_logical_xor_symmetric(self):
        assert chromosome_equal(self.second.logical_xor(self.third), self.third.logical_xor(self.second))

    def test_partial_logical_xor_empty_index_array(self):
        assert chromosome_equal(self.first.partial_logical_xor(self.ones, []), self.first)

    def test_partial_logical_xor(self):
        assert chromosome_equal(self.first.partial_logical_xor(self.second, [0, 1, 2, 3]), self.ones)
        assert chromosome_equal(self.second.partial_logical_xor(self.first, [4, 5, 6, 7]), self.ones)

    def test_partial_logical_xor_asymmetric(self):
        assert not chromosome_equal(self.second.partial_logical_xor(self.third, [1, 3, 5, 7]),
                                    self.third.partial_logical_xor(self.second, [1, 3, 5, 7]))

    def test_combine_with_make_chromosome(self):
        def function(c1, c2):
            return make_chromosome(c1.genes + c2.genes)

        assert chromosome_equal(self.first.combine(self.second, function),
                                make_chromosome(self.first.genes + self.second.genes))

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

    def test_make_random_chromosome_size(self):
        chromosome = make_random_chromosome(32)
        assert len(chromosome) == 32

    def test_make_random_chromosome_randomness(self):
        chromosome1 = make_random_chromosome(200)
        chromosome2 = make_random_chromosome(200)
        assert not chromosome_equal(chromosome1, chromosome2)

    @pytest.mark.parametrize("precision,results", [
        (0, [15, 240, 170, 255, 0]), (8, [0.05859375, 0.9375, 0.6640625, 0.99609375, 0]),
        (1, [7.5, 120, 85, 127.5, 0]), (2, [3.75, 60, 42.5, 63.75, 0]),
        (3, [1.875, 30, 21.25, 31.875, 0]), (4, [0.9375, 15, 10.625, 15.9375, 0])])
    def test_decode(self, precision, results):
        assert self.first.decode(precision) == results[0]
        assert self.second.decode(precision) == results[1]
        assert self.third.decode(precision) == results[2]
        assert self.ones.decode(precision) == results[3]
        assert self.zeros.decode(precision) == results[4]
