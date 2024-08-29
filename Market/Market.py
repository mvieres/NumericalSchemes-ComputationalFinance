import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from NumericalSchemes.TimeGrid import TimeGrid


class Market:
    """
    This class assumes a constant risk-free return rate of the money market account at first.
    For the given timegrid, the risk-free rate can be evaluated at tenor points. TODO: This is not yet implemented
    """
    def __init__(self, tStart: float, tEnd: float, s0: float, r: float):
        """
        :param tStart: float, start time
        :param tEnd: float, end time
        :param s0: float, initial stock price
        :param r: float, risk-free rate, this will be the constant risk-free return rate of the money market account
        """
        assert tStart < tEnd, "Start time must be less than end time"
        self.tStart = tStart
        self.tEnd = tEnd
        self.time_grid_instance = TimeGrid(tStart, tEnd)
        assert s0 > 0, "Initial stock price must be positive"
        self.s0 = s0
        assert r > 0, "Risk-free rate must be positive"
        self.r = r
        self.underlying = {}
        pass

    def computeSolutionPath(self, nSteps: int) -> np.array:
        pass

    def plot_underlying(self, n_steps):
        for key in self.underlying.keys():
            plt.plot(self.time_grid_instance.get_time_grid(n_steps), self.underlying[key], label=key)
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()


class Heston:

    def __init__(self, tStart: float, tEnd: float, s0: float, r: float, v0: float,
                 kappa: float, theta: float, sigma: float, rho: float, scheme: str = "euler"):
        self.tStart = tStart
        self.tEnd = tEnd
        assert s0 > 0, "Initial stock price must be positive"
        self.s0 = s0
        assert r > 0, "Risk-free rate must be positive"
        self.r = r
        assert v0 > 0, "Initial volatility must be positive"
        self.v0 = v0
        assert kappa > 0, "Mean reversion rate must be positive"
        self.kappa = kappa
        assert theta >= 0, "Long-term volatility must be non negative"
        self.theta = theta
        assert sigma >= 0, "Volatility of volatility must be non negative"
        self.sigma = sigma
        self.fellerCondition = self.checkFellercondition()
        self.scheme = scheme
        assert -1 <= rho <= 1, "Correlation coefficient must be between -1 and 1"
        self.rho = rho

    def computeSolutionPath(self, nSteps: int) -> np.array:
        pass

    def checkFellercondition(self) -> bool:
        return 2 * self.kappa * self.theta > self.sigma ** 2
