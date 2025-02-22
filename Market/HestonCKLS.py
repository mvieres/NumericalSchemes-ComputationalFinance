import numpy as np

from Market.HestonCIR import HestonCIR
from NumericalSchemes.SdeSolver import SdeSolver
from PortfolioEvaluation.Params.HestonCKLSParams import HestonCKLSParams


class HestonCKLS(HestonCIR):

    def __init__(self, t_start: float, t_end:float, s0: float, v0: float, r: float, kappa: float,
                 theta: float, sigma: float,rho: float, gamma: float, scheme: str):
        super().__init__(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, scheme)
        self.gamma = gamma
        self.drift_s = lambda t, x: self.r * x[0]
        self.diffusion_s = lambda t, x: self.sigma * np.sqrt(x[1])
        self.drift_v = lambda t, x: self.kappa * (self.theta - x)
        self.diffusion_v = lambda t, x: self.sigma * x**self.gamma
        self.dimension = 2

    def compute_solution_path(self, n_steps: int, bm_path=None) -> np.array:
        """
        Compute the solution path of the Heston-CIR model
        """
        # get volatility
        solver_cir = SdeSolver(self.time_grid_instance, self.drift_v, self.diffusion_v, self.v0)
        _, bm_path, sol = self.solver_instance.init_for_schemes(n_steps, bm_path, [self.s0, self.v0])
        sol[:, 1] = solver_cir.absolute_euler(n_steps, bm_path=bm_path[:, 1])  # volatility here; by flawed design, the timegrid instance is created multiple times, which is not used but does not really cost much performance
        # employ normal Euler for stock price
        for i in range(1, n_steps):
            delta_t = self.time_grid_instance.get_time_grid(n_steps)[i] - self.time_grid_instance.get_time_grid(n_steps)[i - 1]
            delta_bm = bm_path[i] - bm_path[i - 1]
            sol[i, 0] = sol[i - 1, 0] + self.drift_s(self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_t + \
                        self.diffusion_s(self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_bm[0] + \
                        self.diffusion_s(self.time_grid_instance.get_time_grid(n_steps)[i - 1], sol[i - 1]) * delta_bm[1]
        return sol

    def pull_params(self, params: HestonCKLSParams):
        super().pull_params(params)
        self.gamma = params.get_gamma()
