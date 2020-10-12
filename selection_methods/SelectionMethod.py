class SelectionMethod:
    part_of_guarded = 0
    search_minimum = False

    def __init__(self, part_of_guarded, search_minimum=False):
        self.part_of_guarded = part_of_guarded
        self.search_minimum = search_minimum

    def select_next_generation(self, population, population_evaluate):
        raise NotImplementedError

    def save_elite(self, population, population_evaluate):
        survivors_number = round(population.population_size * self.part_of_guarded)
        if not self.search_minimum:
            elite_survivors_indexes = population_evaluate.argsort()[-survivors_number:]
        else:
            elite_survivors_indexes = population_evaluate.argsort()[:survivors_number]
        return elite_survivors_indexes
