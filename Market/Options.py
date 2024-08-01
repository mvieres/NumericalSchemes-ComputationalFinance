import numpy as np


class Options:
    """

    """
    @staticmethod
    def call(x, k):
        return np.maximum(0, x - k)

    @staticmethod
    def put(x, k):
        return np.maximum(0, k - x)

    @staticmethod
    def arithmetic_asian_call(x, k, n):
        return np.max((1 / n) * np.sum(x - k), 0)
