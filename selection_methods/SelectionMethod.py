class SelectionMethod:
    part_of_guarded = 0

    def select_next_generation(self, population, population_evaluate):
        self.__save_elite()

    def __save_elite(self):
        raise NotImplementedError
