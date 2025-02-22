import unittest

from Market.BlackScholes import BlackScholes
from Market.CIR import CIR
from Market.CKLS import CKLS
from Pricing.MonteCarlo.StandardMonteCarlo import StandardMonteCarlo


class StandardMonteCarloTest(unittest.TestCase):

    def test_functionality(self):
        blackscholes_instance = BlackScholes(0, 1, 100, 0.01, 0.0001, "absolute_euler")
        cir = CIR(0, 1, 0.01, 0.01, 0.01, 0.01, "absolute_euler")
        fx = CKLS(0, 1, 100, 0.01, 0.01, 0.01, 0.6, "absolute_euler")
        pricing = StandardMonteCarlo(underlying_instance=blackscholes_instance, payoff="call",
                                     payoff_params={"strike": 100}, n_paths=100, n_steps=100,
                                     discount_curve=cir, fx_curve=fx)
        try:
            price = pricing.compute_option_price()
            self.assertTrue(price >= 0)
        except Exception as e:
            self.fail("Standard-Monte carlo failed due to: " + str(e))

    def compare_with_exact_solution(self):
        """
        Compare simple call option with exact solution with constant interest rate.

        @return:
        """

        pass


if __name__ == '__main__':
    unittest.main()
