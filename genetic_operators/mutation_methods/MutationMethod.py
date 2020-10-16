class MutationMethod:
    mutation_probability = None

    def __init__(self, mutation_probability):
        self.mutation_probability = mutation_probability

    def mutate_population(self):
        raise NotImplementedError
