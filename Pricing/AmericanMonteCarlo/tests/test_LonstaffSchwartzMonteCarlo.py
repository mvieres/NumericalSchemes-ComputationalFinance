import unittest
import numpy as np

from Pricing.AmericanMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo as lsmc
from Market.BlackScholes import BlackScholes
from Market.Heston import Heston
from Pricing.TheoreticalPrices import BlackScholesOptionPrices


class LongstaffSchwartzMonteCarloTest(unittest.TestCase):
    """

        TODO: LSMC returns wrong values. Can be checked via Put-Call Parity with respect to American-European options.
    """
    def test_lsm_init(self):
        bs_instance = BlackScholes(0, 1, 100, 0.05, 0.2)
        lsm_instance = lsmc(bs_instance, lambda x: np.maximum(100 - x, 0), 10, 100)
        self.assertTrue(True)

    def test_dict_convertion(self):
        # Example dictionary
        example_dict = {1: [0, 1, 2, 4], 2: [5, 4, 3, 4], 3: [1, 1, 1, 4]}
        asset_price = np.zeros(shape=(3, 4))
        for key in example_dict.keys():
            asset_price[key] = example_dict[key]

    def test_functionality_black_scholes(self):
        t_start = 0
        t_end = 1
        r = 0.06
        sigma = 0.2
        s0 = 36
        strike = 33
        bs_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma)
        n_paths = 10
        n_steps = 10
        payoff = lambda x: np.maximum(x - strike, 0)
        try:
            lsm_instance = lsmc(bs_instance, payoff=payoff, n_paths=n_paths, n_steps=n_steps)
            lsm_instance.compute_option_price()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error: {e} was raised")

    def test_theoretical_value_black_scholes(self):
        t_start = 0
        t_end = 1
        r = 0.06
        sigma = 0.2
        s0 = 36
        strike = 33
        bs_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma)
        n_paths = 30000
        n_steps = 1000
        payoff = lambda x: np.maximum(strike - x, 0)
        lsm_instance = lsmc(bs_instance, payoff=payoff, n_paths=n_paths, n_steps=n_steps)
        lsm_instance.compute_option_price()
        theoretical_instance = BlackScholesOptionPrices(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma)
        theoretical_call_price = theoretical_instance.call_option_theoretical_price(strike)
        epsilon = 0.5
        self.assertTrue(theoretical_call_price - epsilon < lsm_instance.value_0 < theoretical_call_price + epsilon)

    def test_functionality_heston(self):
        # TODO: Look up how to implement this properly (try-catch-block?)

        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
