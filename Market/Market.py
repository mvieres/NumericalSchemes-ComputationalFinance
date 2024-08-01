import numpy as np
from scipy.stats import norm
from NumericalSchemes.TimeGrid import TimeGrid
from NumericalSchemes.SdeSolver import SdeSolver


class BlackScholes:

    def __init__(self, tStart: float, tEnd: float, s0: float, r: float, sigma: float, scheme: str = "euler"):
        self.tStart = tStart
        self.tEnd = tEnd
        assert s0 > 0, "Initial stock price must be positive"
        self.s0 = s0
        assert r > 0, "Risk-free rate must be positive"
        self.r = r
        assert sigma >= 0, "Volatility must be non negative"
        self.sigma = sigma
        self.scheme = scheme
        self.timeGridInstance = TimeGrid(tStart, tEnd)

    def callOptionTheoreticalPrice(self, k: float, seed=None) -> float:
        """
        Theoretical price of european call option with maturity at tEnd and strike price k at time tStart
        @param k:
        @return:
        """
        if seed is not None:
            np.random.seed(seed)
        d1 = (np.log(self.s0 / k) + (self.r + 0.5 * self.sigma ** 2) * (self.tEnd - self.tStart)) / (
                    self.sigma * np.sqrt(self.tEnd - self.tStart))
        d2 = d1 - self.sigma * np.sqrt(self.tEnd - self.tStart)
        return self.s0 * norm.cdf(d1) - k * np.exp(-self.r * (self.tEnd - self.tStart)) * norm.cdf(d2)

    def computeSolutionPath(self, nSteps: int) -> np.array:
        drift = lambda t, x: self.r * x
        diffusion = lambda t, x: self.sigma * x
        diffusion_derivative = lambda t, x: self.sigma

        schemes = {
            "euler": SdeSolver.euler,
            "absoluteEuler": SdeSolver.absoluteEuler,
            "milstein": SdeSolver.milstein
        }

        if self.scheme in schemes:
            if self.scheme == "milstein":
                return schemes[self.scheme](self.timeGridInstance, nSteps, np.array([self.s0]), drift, diffusion,
                                            diffusion_derivative)
            else:
                return schemes[self.scheme](self.timeGridInstance, nSteps, np.array([self.s0]), drift, diffusion)
        else:
            raise ValueError("Scheme not implemented")


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
