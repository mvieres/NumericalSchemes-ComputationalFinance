import numpy as np

from Market.AbstractMarket import AbstractMarket
from NumericalSchemes.SdeSolver import SdeSolver


class CIR(AbstractMarket):

    def __init__(self, t_start, t_end, x0, theta, kappa, sigma, scheme: str):
        super().__init__(t_start, t_end, x0)
        self.theta = theta
        self.kappa = kappa
        self.sigma = sigma
        self.scheme = scheme
        self.drift = lambda t, x: self.kappa * (self.theta - x)
        self.diffusion = lambda t, x: self.sigma * np.sqrt(x)
        self.solver_instance = SdeSolver(self.time_grid_instance, self.drift, self.diffusion, x0)
        self.schemes = {
            "absolute_euler": self.solver_instance.absolute_euler,
        }
        self.dimension = 1
        assert scheme in self.schemes.keys(), "The scheme is not valid"

    def compute_solution_path(self, n_steps: int) -> np.array:
        return self.schemes[self.scheme](n_steps)

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path(n_steps)
