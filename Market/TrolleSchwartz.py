import numpy as np

from Market.AbstractMarket import AbstractMarket
from NumericalSchemes.SdeSolver import SdeSolver


class TrolleSchwartz(AbstractMarket):
    """
    TrolleSchwartz implements the TrolleSchwartz model for N=1.
    Its purpose is to model the time-t forward rate for lending time T.
    The model is characterized by its SDE as follows:
    df(t,T) = mu_f(t,T) dt + sigma_{f,i}(t,T) sqrt(v_t) dW^{Q}(t)
    dv(t) = kappa*(theta - v(t)) dt + sigma * sqrt(v(t)) ( rho dW^{Q}(t) + sqrt(1-rho^2) dZ^{Q}(t) )
    where W^{Q} and Z^{Q} are independent Brownian motions under the risk-neutral measure Q.
    sigma_{f,i}(t,T) is supposed to be the forward rate volatility function.
    To keep the computatuon simple, this forward rate volatility is given by a fixed formula:
    simga_{f,i}(t,T) = (alpha_0 + alpha_1*(T-t))*exp(-gamma*(T-t)).
    # TODO: not clear if t_start has to be specified; paper implies interval [0,T]. Not clear if this curve viewd on [t,T] is the same as a simulation started at t.
    """
    def __init__(self,t_start, t_end,r: float, alpha_0: float, alpha_1: float, gamma: float, kappa: float, theta: float, sigma: float, rho: float, scheme:str):
        super().__init__(t_start, t_end, r, r)  # TODO: s0 is not used in the model -> review initialization
        self.dimension = 2
        self.scenarios = {}
        self.scenarios = self.underlying
        self.scheme = scheme
        self.alpha_0 = alpha_0
        self.alpha_1 = alpha_1
        self.gamma = gamma
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.v0 = r * 0.1  # TODO: not clear if this is a good choice
        self.drift_vol = lambda t, x: self.kappa*(self.theta - x[1])
        self.diffusion_vol = {1: lambda t, x: self.rho*self.sigma*np.sqrt(x[1]), 2: lambda t, x: np.sqrt(1-rho**2)*sigma*np.sqrt(x[1])}
        self.integral_term = lambda t, x: ((self.alpha_0 / self.gamma)*(1-np.exp(-self.gamma*(self.t_end-t)))
                                     - (self.alpha_1 / self.gamma)*(self.t_end - t)*np.exp(-self.gamma*(self.t_end-t))
                                     + (self.alpha_1 / self.gamma**2)*(1-np.exp(-self.gamma*(self.t_start-t))))
        self.sigma_f = lambda t, x: (self.alpha_0 + self.alpha_1*(self.t_end-t))*np.exp(-self.gamma*(self.t_end-t))
        self.drift_f = lambda t, x:  x[1]* self.sigma_f(t, x) * self.integral_term(t, x)
        self.diffusion_f = {1: lambda t, x: self.sigma_f(t, x)*np.sqrt(x[1])}
        self.drift = {1: self.drift_f, 2: self.drift_vol}
        self.diffusion = {1: self.diffusion_f, 2: self.diffusion_vol}
        solver_instance = SdeSolver(time_grid_instance=self.time_grid_instance, drift=self.drift,
                                    diffusion=self.diffusion, starting_point=[self.r, self.v0], order_dimensions=[2, 1])
        self.schemes = {'absolute_euler': solver_instance.absolute_euler}
        assert scheme in self.schemes.keys(), f"Scheme {scheme} not implemented (or typo)"

    def compute_solution_path(self, n_steps: int) -> np.array:
        # TODO: absolute euler for first dimension implies that interest rate cannot be negative. This is i.a. not the case
        return self.schemes[self.scheme](n_steps)

    def generate_scenarios(self, n_paths: int, n_steps: int) -> None:
        for i in range(n_paths):
            self.scenarios[i] = self.compute_solution_path(n_steps)