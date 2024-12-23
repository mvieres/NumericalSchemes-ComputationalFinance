from NumericalSchemes.RandomProcesses import RandomProcesses
from NumericalSchemes.SdeSolver import SdeSolver
from Market.AbstractMarket import AbstractMarket

import numpy as np

from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams


class BlackScholes(AbstractMarket):
    """


    """
    def __init__(self, t_start: float, t_end: float, s0: float, r: float, sigma: float, scheme: str = "euler", sim_type="normal"):
        self.t_start = t_start
        self.t_end = t_end
        super().__init__(t_start, t_end, s0, r)
        self.s0 = s0
        self.dimension = 1
        assert sigma >= 0, "Volatility must be non negative"
        self.sigma = sigma
        self.scheme = scheme
        self.scenarios = {}  # Stores different paths; i.e. one sample path = one scenario
        self.sim_type = sim_type
        if sim_type == "normal":
            self.drift = lambda t, x: r * x
        else:
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

    def compute_solution_path_exact(self, n_steps):
        bm = RandomProcesses.brownian_motion_path(self.time_grid_instance, n_steps, 1)
        x = np.zeros(n_steps)
        x[0] = self.s0
        for i in range(1, n_steps):
            x[i] = self.s0 * np.exp((self.r - 0.5 * self.sigma ** 2) * self.time_grid_instance.get_time_grid(n_steps)[i] + self.sigma * bm[i])
        return x

    def generate_scenarios_exact(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path_exact(n_steps)

    def get_sigma(self):
        return self.sigma

    def set_sigma(self, sigma):
        self.sigma = sigma

    def pull_params(self, params: BlackScholesParams):
        self.set_r(params.get_r())
        self.set_sigma(params.get_sigma())
        self.set_s0(params.get_starting_point())
        self.set_t_start(params.get_t_start())
        self.set_t_end(params.get_t_end())
