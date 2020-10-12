from genetic_operators.crossover_methods import CrossingMethod


# todo one/two/three point crossing
class PointCrossing(CrossingMethod):
    def crossover_population(self, population):
        raise NotImplementedError
