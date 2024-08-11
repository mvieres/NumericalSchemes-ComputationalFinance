import numpy as np


class EuropeanOptions:
    """

    """
    @staticmethod
    def call(x: float, k: float) -> float:
        return np.maximum(0, x - k)

    @staticmethod
    def put(x: float, k: float) -> float:
        return np.maximum(0, k - x)

    @staticmethod
    def arithmetic_asian_call(x: float, k: float, n: int) -> float:
        return np.max((1 / n) * np.sum(x - k), 0)
