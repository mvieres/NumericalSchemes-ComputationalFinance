import numpy as np
from scipy.stats import norm

from Market.BlackScholes import BlackScholes


class BlackScholesOptionPrices(BlackScholes):
    """
    TODO: Not clear if this class should have a constructor at all -> maybe usage of only static methods
    """
    def __init__(self, tStart: float, tEnd: float, s0: float, r: float, sigma: float, scheme: str = "euler"):
        super().__init__(tStart, tEnd, s0, r, sigma, scheme)

    def call_option_theoretical_price(self, k: float, s0=None) -> float:
        """
        Theoretical price of european call option with maturity at tEnd and strike price k at time tStart
        @param s0:
        @param k:
        @return:
        """
        if s0 is None:
            s0 = self.s0
        d1 = (np.log(s0 / k) + (self.r + 0.5 * self.sigma ** 2) * (self.tEnd - self.tStart)) / (
                    self.sigma * np.sqrt(self.tEnd - self.tStart))
        d2 = d1 - self.sigma * np.sqrt(self.tEnd - self.tStart)
        return s0 * norm.cdf(d1) - k * np.exp(-self.r * (self.tEnd - self.tStart)) * norm.cdf(d2)

    def put_option_theoretical_price(self, k: float, s0=None) -> float:
        """
        Theoretical price of european put option with maturity at tEnd and strike price k at time tStart
        @param s0:
        @param k:
        @return:
        """
        if s0 is None:
            s0 = self.s0
        d1 = (np.log(s0 / k) + (self.r + 0.5 * self.sigma ** 2) * (self.tEnd - self.tStart)) / (
                    self.sigma * np.sqrt(self.tEnd - self.tStart))
        d2 = d1 - self.sigma * np.sqrt(self.tEnd - self.tStart)
        return k * np.exp(-self.r * (self.tEnd - self.tStart)) * norm.cdf(-d2) - s0 * norm.cdf(-d1)


class TrolleSchwartz:
    """
    Theoretical prices for bond options when priced under the risk neutral measure and the TrolleSchwartz model.
    """
    def __init__(self):
        pass
