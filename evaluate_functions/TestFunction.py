import numpy as np

from evaluate_functions.EvaluateFunction import EvaluateFunction


class TestFunction(EvaluateFunction):
    def evaluate(self, values):
        x1 = values[0]
        x2 = values[1]
        # fact1 = math.cos(math.sin(math.fabs(x1**2-x2**2))) - 0.5
        # fact1 = np.cos(np.sin(np.fabs(x1 ** 2 - x2 ** 2))) - 0.5
        # fact2 = (1 + 0.001 * (x1 ** 2 + x2 ** 2)) ** 2
        # y = 0.5 + fact1 / fact2;
        y = x1 ** 2 + (x2 - 5) ** 2 + 6
        return y

    def getValuesNumber(self):
        return 2
