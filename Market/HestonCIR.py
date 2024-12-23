import numpy as np

from Market.AbstractMarket import AbstractMarket
from NumericalSchemes.SdeSolver import SdeSolver
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams


class HestonCIR(AbstractMarket):
    """Simulation of Heston-CIR model (stochastic volatility model)"""
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
        self.drift = {2: lambda t, x: self.kappa * (self.theta - x[1]), 1: lambda t, x: self.r * x[0]}
        self.diffusion = {1: {1: lambda t, x: self.rho * np.sqrt(x[1]) * x[0],
                              2: lambda t, x: np.sqrt(1-(self.rho**2))*np.sqrt(x[1])*x[0]},
                          2: {1: lambda t, x: self.sigma * np.sqrt(x[1])}}

        self.solver_instance = SdeSolver(time_grid_instance=self.time_grid_instance,
                                         drift=self.drift, diffusion=self.diffusion, starting_point=[s0, v0])
        self.solver_instance.set_order([2, 1])
        self.schemes = {
            "absolute_euler": self.solver_instance.absolute_euler,
        }

    def compute_solution_path(self, n_steps: int) -> np.array:
        return self.schemes[self.scheme](n_steps)

    def check_fellercondition(self) -> bool:
        return 2 * self.kappa * self.theta > self.sigma ** 2

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path_old(n_steps=n_steps)

    #def plot_underlying(self):
     #   super().plot_underlying()

    def pull_params(self, params: HestonCIRParams):
        super().s0 = params.get_starting_point()
        self.v0 = params.get_v0()
        super().r = params.get_r()
        self.kappa = params.get_kappa()
        self.theta = params.get_theta()
        self.sigma = params.get_sigma()
        self.rho = params.get_rho()

    def compute_solution_path_old(self, n_steps: int, bm_path=None) -> np.array:
        """
        Compute the solution path of the Heston-CIR model
        """
        drift_v = lambda t, x: self.kappa * (self.theta - x)
        diffusion_v = lambda t, x: self.sigma * np.sqrt(x)
        drift_s = self.drift[1]
        diffusion_s = self.diffusion[1]
        assert isinstance(diffusion_s, dict), "Diffusion must be dict"
        # get volatility
        solver_cir = SdeSolver(self.time_grid_instance, drift_v, diffusion_v, self.v0)
        _, bm_path, sol = self.solver_instance.init_for_schemes(n_steps, bm_path, [self.s0, self.v0])
        sol[:, 1] = solver_cir.absolute_euler(n_steps, bm_path=bm_path[:, 1])  # volatility here; by flawed design, the timegrid instance is created multiple times, which is not used but does not really cost much performance
        # employ normal Euler for stock price
        for i in range(1, n_steps):
            delta_t = self.time_grid_instance.get_time_grid(n_steps)[i] - self.time_grid_instance.get_time_grid(n_steps)[i - 1]
            delta_bm = bm_path[i] - bm_path[i - 1]
            sol[i, 0] = sol[i - 1, 0] + drift_s(self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_t + \
                        diffusion_s[1](self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_bm[0] + \
                        diffusion_s[2](self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_bm[1]
        return sol