import numpy as np


class OptionUtil:

    @staticmethod
    def call():
        return lambda x, modelparams: np.maximum(x - modelparams, 0)

    @staticmethod
    def put():
        return lambda x, modelparams: np.maximum(modelparams - x, 0)

    @staticmethod
    def arithmetic_call():
        """
        This is the payoff for an arithmetic call option
        """
        return lambda x, modelparams: np.maximum((1/modelparams.get("dt"))*np.mean(x) - modelparams.get("strike"), 0)

    @staticmethod
    def arithmetic_put():
        """
        This is the payoff for an arithmetic put option
        """
        return lambda x, modelparams: np.maximum(modelparams.get("strike") - (1/modelparams.get("dt"))*np.mean(x), 0)
