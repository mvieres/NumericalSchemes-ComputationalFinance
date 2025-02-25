import unittest
import numpy as np

from Market.HestonCKLS import HestonCKLS
from Pricing.AmericanMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo as lsmc
from Market.BlackScholes import BlackScholes
from Market.HestonCIR import HestonCIR
from Pricing.TheoreticalPrices import BlackScholesOptionPrices
from analysis.supported_payoffs import supported_payoffs, classification


class LongstaffSchwartzMonteCarloTest(unittest.TestCase):
    """

        TODO: LSMC returns wrong values. Can be checked via Put-Call Parity with respect to American-European options.
    """

    def test_functionality_black_scholes(self):
        t_start = 0
        t_end = 1
        r = 0.06
        sigma = 0.2
        s0 = 36
        strike = 33
        bs_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma)
        n_paths = 2
        n_steps = 4
        try:
            lsm_call_instance = lsmc(bs_instance, payoff="put", n_paths=n_paths, n_steps=n_steps)
            lsm_call_instance.compute_option_price()
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
        t_start = 0
        t_end = 1
        r = 0.06
        theta = 0.1
        kappa = 0.5
        sigma = 0.2
        rho = -0.4
        s0 = 36
        v0 = 1
        heston_cir_instance = HestonCIR(t_start=t_start, t_end=t_end, s0=s0, r=r, theta=theta, kappa=kappa,
                                sigma=sigma, rho=rho, v0=v0, scheme='absolute_euler')
        gamma = 0.6
        heston_ckls_instance = HestonCKLS(t_start=t_start, t_end=t_end, s0=s0, r=r, theta=theta, kappa=kappa,
                                sigma=sigma, rho=rho, v0=v0, gamma=gamma, scheme='absolute_euler')
        n_paths = 10
        n_steps = 30
        strike = 33
        payoff = lambda x: np.maximum(x - strike, 0)
        try:
            lsm1_instance = lsmc(heston_cir_instance, payoff=payoff,
                                 payoff_type="path_independent", n_paths=n_paths, n_steps=n_steps)
            lsm1_instance.compute_option_price()
            lsm2_instance = lsmc(heston_ckls_instance, payoff=payoff,
                                 payoff_type="path_independent", n_paths=n_paths, n_steps=n_steps)
            lsm2_instance.compute_option_price()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error: {e} was raised")


if __name__ == '__main__':
    unittest.main()
