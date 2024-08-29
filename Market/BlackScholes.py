from NumericalSchemes.SdeSolver import SdeSolver
from Market.Market import Market

import numpy as np


class BlackScholes(Market):

    def __init__(self, tStart: float, tEnd: float, s0: float, r: float, sigma: float, scheme: str = "euler"):
        self.tStart = tStart
        self.tEnd = tEnd
        super().__init__(tStart, tEnd, s0, r)  # TODO: wrong initalization
        assert sigma >= 0, "Volatility must be non negative"
        self.sigma = sigma
        self.scheme = scheme
        self.scenarios = {}  # Stores different paths; i.e. one sample path = one scenario
        self.drift = lambda t, x: r * x
        self.diffusion = lambda t, x: self.sigma * x
        self.diffusion_derivative = lambda t, x: self.sigma
        self.solver_instance = SdeSolver(time_grid_instance=self.time_grid_instance,
                                         drift=self.drift, diffusion=self.diffusion, starting_point=s0)
        self.solver_instance.set_diffustion_derivative(self.diffusion_derivative)
        self.underlying = self.scenarios  # TODO: this should be a pointer to the underlying of market class
        self.schemes = {
            "euler": self.solver_instance.euler,
            "absolute_euler": self.solver_instance.absolute_euler,
            "milstein": self.solver_instance.milstein
        }
        assert self.scheme in self.schemes.keys(), "Scheme key error"

    def computeSolutionPath(self, nSteps: int) -> np.array:
        return self.schemes[self.scheme](nSteps)

    def generateScenarios(self, nPaths: int, nSteps: int) -> None:
        for i in range(nPaths):
            self.scenarios[i] = self.computeSolutionPath(nSteps)

    def plot_underlying(self, n_steps):
        super().plot_underlying(n_steps)
