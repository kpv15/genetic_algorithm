from selection_methods.SelectionMethod import SelectionMethod


class TournamentSelection(SelectionMethod):

    def select_next_generation(self, population, population_evaluate):
        super().select_next_generation()
        raise NotImplementedError
