from selection_methods.SelectionMethod import SelectionMethod


class BestSelection(SelectionMethod):
    def select_next_generation(self, population, population_evaluate):
        super().select_next_generation()
        raise NotImplementedError

    def __init__(self, part_of_guarded, search_minimum=False):
        super().__init__(part_of_guarded, search_minimum)
