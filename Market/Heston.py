import numpy as np

from Market.AbstractMarket import AbstractMarket
from NumericalSchemes.SdeSolver import SdeSolver
from PortfolioEvaluation.Params.HestonParams import HestonParams


class Heston(AbstractMarket):
    def __init__(self, t_start: float, t_end: float, s0: float, v0: float,r: float, kappa: float, theta: float, sigma: float, rho: float, scheme: str):
        super().__init__(t_start, t_end, s0, r)
        self.dimension = 2
        assert v0 > 0, "Initial volatility must be positive"
        self.v0 = v0
        assert kappa > 0, "Mean reversion rate must be positive"
        self.kappa = kappa
        assert theta >= 0, "Long-term volatility must be non negative"
        self.theta = theta
        assert sigma >= 0, "Volatility of volatility must be non negative"
        self.sigma = sigma
        self.fellerCondition = self.check_fellercondition()
        self.scenarios = self.underlying
        self.scheme = scheme
        assert -1 <= rho <= 1, "Correlation coefficient must be between -1 and 1"
        self.rho = rho
        drift = {2: lambda t, x: self.kappa * (self.theta - x[1]), 1: lambda t, x: self.r * x[0]}
        diffustion = {1: {1: lambda t, x: self.rho*np.sqrt(x[1])*x[0],
                          2: lambda t, x: np.sqrt(1-(self.rho**2))*np.sqrt(x[1])*x[0]},
                      2: {1: lambda t, x: self.sigma * np.sqrt(x[1])}}

        self.solver_instance = SdeSolver(time_grid_instance=self.time_grid_instance,
                                         drift=drift, diffusion=diffustion, starting_point=[s0, v0])
        self.solver_instance.set_order([2, 1])
        self.schemes = {
            "euler": self.solver_instance.euler,  # TODO: Euler is bullshit for Heston
            "absolute_euler": self.solver_instance.absolute_euler,
        }
        pass

    def compute_solution_path(self, nSteps: int) -> np.array:
        return self.schemes[self.scheme](nSteps)

    def check_fellercondition(self) -> bool:
        return 2 * self.kappa * self.theta > self.sigma ** 2

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path(n_steps)

    def plot_underlying(self):
        super().plot_underlying()

    def pull_params(self, params: HestonParams):
        self.s0 = params.get_s0()
        self.v0 = params.get_v0()
        self.r = params.get_r()
        self.kappa = params.get_kappa()
        self.theta = params.get_theta()
        self.sigma = params.get_sigma()
        self.rho = params.get_rho()
