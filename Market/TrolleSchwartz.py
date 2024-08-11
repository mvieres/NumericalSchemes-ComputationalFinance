

class TrolleSchwartz:
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
    def __init__(self):
        self.forward_rate = {}
        pass

    def compute_forward_rate(self, t_start: float, T: float):
        pass

    def get_forward_rate(self, t_start: float, t: float, T: float):
        pass

    def get_short_rate(self,t_start: float, T: float):
        self.get_forward_rate(t_start, 0, T)
