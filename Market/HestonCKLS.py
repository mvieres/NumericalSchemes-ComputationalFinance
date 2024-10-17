import numpy as np

from Market.HestonCIR import HestonCIR
from PortfolioEvaluation.Params.HestonCKLSParams import HestonCKLSParams


class HestonCKLS(HestonCIR):

    def __init__(self, t_start: float, t_end:float, s0: float, v0: float, r: float, kappa: float,
                 theta: float, sigma: float,rho: float, gamma: float, scheme: str):
        super().__init__(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, scheme)
        self.gamma = gamma
        self.drift_s = lambda t, x: self.r * x[0]
        self.diffusion_s = lambda t, x: self.sigma * np.sqrt(x[1])

    def compute_solution_path(self, n_steps: int):
        """
        Compute the solution path of the HestonCKLS model by solving the volatility process first and then using
        basic euler for the spot price
        """



    def pull_params(self, params: HestonCKLSParams):
        super().pull_params(params)
        self.gamma = params.get_gamma()