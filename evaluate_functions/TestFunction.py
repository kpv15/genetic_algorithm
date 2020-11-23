from evaluate_functions.EvaluateFunction import EvaluateFunction
from model.elements import Individual


class TestFunction(EvaluateFunction):
    @staticmethod
    def evaluate(values: Individual):
        x1 = values.chromosomes.values()['x1'].docode()
        x2 = values.chromosomes.values()['x2'].docode()
        # fact1 = math.cos(math.sin(math.fabs(x1**2-x2**2))) - 0.5
        # fact1 = np.cos(np.sin(np.fabs(x1 ** 2 - x2 ** 2))) - 0.5
        # fact2 = (1 + 0.001 * (x1 ** 2 + x2 ** 2)) ** 2
        # y = 0.5 + fact1 / fact2;
        y = x1 ** 2 + (x2 - 5) ** 2 + 6
        return y

    def getParameterNumber(self):
        return len(self.getParameterNames())

    @staticmethod
    def getParameterNames():
        return ['x1', 'x2']
