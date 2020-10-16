import random

import numpy as np


class CrossingMethod:
    mutation_probability = None

    def __init__(self, mutation_probability):
        self.mutation_probability = mutation_probability

    def cross_population(self, population):
        members_to_cross = []
        for populationMember in population:
            if self.mutation_probability > np.random.random():
                members_to_cross.append(populationMember)
            else:
                population.add_next_generation_member(populationMember)
        if len(members_to_cross) % 2 != 0:
            i = random.randrange(len(members_to_cross))
            population.add_next_generation_member(members_to_cross.pop(i))
        while len(members_to_cross) > 0:
            x = members_to_cross.pop(random.randrange(len(members_to_cross)))
            y = members_to_cross.pop(random.randrange(len(members_to_cross)))
            x, y = self.cross_pair((x, y))
            population.add_next_generation_member(x)
            population.add_next_generation_member(y)
        population.change_of_generations()

    def cross_pair(self, generation_members_pair: object):
        raise NotImplementedError
