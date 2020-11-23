class EvaluateFunction:
    def evaluate(self, values):
        raise NotImplementedError

    def getParameterNumber(self):
        return len(self.getParameterNames())

    def getParameterNames(self):
        raise NotImplementedError
