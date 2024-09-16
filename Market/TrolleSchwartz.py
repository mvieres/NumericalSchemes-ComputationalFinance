import numpy as np

from Market.AbstractMarket import AbstractMarket


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
    def __init__(self,t_start, t_end, alpha_0: float, alpha_1: float, gamma: float, kappa: float, theta: float, sigma: float, rho: float):
        super().__init__(t_start, t_end, 0, None)
        self.alpha_0 = alpha_0
        self.alpha_1 = alpha_1
        self.gamma = gamma
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        drift = {1: lambda t, x: self.x[1] * (self.alpha_0 +
                                              self.alpha_1 * (self.t_end - t)) * np.exp(-self.gamma * (self.t_end - t)) * integral_term, 2: lambda t, x: 0}
        pass

    def compute_solution_path(self, nSteps: int) -> np.array:
        pass
