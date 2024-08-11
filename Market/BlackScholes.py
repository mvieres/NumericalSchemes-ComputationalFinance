from NumericalSchemes.SdeSolver import SdeSolver
from NumericalSchemes.TimeGrid import TimeGrid
from Market.Market import Market
import numpy as np


class BlackScholes(Market):

    def __init__(self, tStart: float, tEnd: float, s0: float, r: float, sigma: float, scheme: str = "euler"):
        self.tStart = tStart
        self.tEnd = tEnd
        super().__init__(s0, r)
        assert sigma >= 0, "Volatility must be non negative"
        self.sigma = sigma
        self.scheme = scheme
        self.timeGridInstance = TimeGrid(tStart, tEnd)
        self.scenarios = {}  # Stores different paths; i.e. one sample path = one scenario
        self.drift = lambda t, x: super().r * x
        self.diffusion = lambda t, x: self.sigma * x
        self.diffusion_derivative = lambda t, x: self.sigma
        self.schemes = {
            "euler": SdeSolver.euler,
            "absoluteEuler": SdeSolver.absoluteEuler,
            "milstein": SdeSolver.milstein
        }

    def computeSolutionPath(self, nSteps: int) -> np.array:
        if self.scheme in self.schemes:
            if self.scheme == "milstein":
                return self.schemes[self.scheme](self.timeGridInstance, nSteps, np.array([self.s0]), self.drift, self.diffusion,
                                            self.diffusion_derivative)
            else:
                return self.schemes[self.scheme](self.timeGridInstance, nSteps, np.array([self.s0]), self.drift, self.diffusion)
        else:
            raise ValueError("Scheme not implemented")

    def generateScenarios(self, nPaths: int, nSteps: int) -> None:
        for i in range(nPaths):
            self.scenarios[i] = self.computeSolutionPath(nSteps)
