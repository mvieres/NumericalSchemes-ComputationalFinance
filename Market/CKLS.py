import numpy as np

from Market.AbstractMarket import AbstractMarket
from NumericalSchemes.SdeSolver import SdeSolver


class CKLS(AbstractMarket):

    def __init__(self, t_start, t_end, x0, theta, kappa, sigma, gamma, scheme:str):
        super().__init__(t_start, t_end, x0, 0)
        self.kappa = kappa
        self.sigma = sigma
        self.theta = theta
        self.gamma = gamma
        self.scheme = scheme
        self.scenarios = {}
        if self.scheme == "drift_implicid_euler":
            self.drift = lambda t, x: (1-self.gamma) * (self.kappa * self.theta * x**(-self.gamma / (1-self.gamma)) - self.kappa*x - ((self.gamma*self.sigma**2 / 2) * x**(-1)))
            self.diffusion = lambda t, x: (1-self.gamma)*self.sigma
            self.solver_instance = SdeSolver(self.time_grid_instance, self.drift, self.diffusion, self.drift(0,x0))
        else:
            self.drift = lambda t, x: self.kappa * (self.theta - x)
            self.diffusion = lambda t, x: self.sigma * np.sqrt(x)
            self.solver_instance = SdeSolver(self.time_grid_instance, self.drift, self.diffusion, x0)
        self.schemes = {
            "absolute_euler": self.solver_instance.absolute_euler,
            #"drift_implicid_euler": self.solver_instance.drift_implicit_euler, Turned off for the moment
        }
        assert scheme in self.schemes.keys(), "The scheme is not valid"

    def compute_solution_path(self, n_steps: int) -> np.array:
        return self.schemes[self.scheme](n_steps)

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path(n_steps)
