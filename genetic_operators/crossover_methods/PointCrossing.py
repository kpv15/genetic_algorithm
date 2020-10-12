from genetic_operators.crossover_methods.CrossingMethod import CrossingMethod
# todo one/two/three point crossing


class PointCrossing(CrossingMethod):
    def cross_population(self, population):
        raise NotImplementedError
