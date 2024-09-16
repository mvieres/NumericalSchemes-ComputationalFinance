from NumericalSchemes.SdeSolver import SdeSolver
from Market.AbstractMarket import AbstractMarket

import numpy as np


class BlackScholes(AbstractMarket):

    def __init__(self, t_start: float, t_end: float, s0: float, r: float, sigma: float, scheme: str = "euler"):
        self.tStart = t_start
        self.tEnd = t_end
        super().__init__(t_start, t_end, s0, r)
        self.dimension = 1
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

    def compute_solution_path(self, nSteps: int) -> np.array:
        return self.schemes[self.scheme](nSteps)

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path(n_steps)

    def plot_underlying(self):
        super().plot_underlying()
