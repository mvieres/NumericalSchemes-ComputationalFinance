import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
from Market.BlackScholes import BlackScholes


class BlackScholesTest(unittest.TestCase):

    def test_init(self):
        blackscholes_instance = BlackScholes(0, 5, 100, 0.01, 0.5, "milstein")
        blackscholes_instance.generate_scenarios(8, 1000)
        blackscholes_instance.plot_underlying()

    def test_functionality(self):
        blackscholes_instance = BlackScholes(0, 5, 100, 0.01, 0.5, "milstein")
        blackscholes_instance.generate_scenarios(8, 1000)
        try:
            blackscholes_instance.generate_scenarios(8, 10)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error: {e} was raised")

    def test_distribution(self):
        t_start = 0
        t_end = 1
        s0 = 100
        r = 0.05
        sigma = 0.2
        n_steps = 100
        n_paths = 10000
        blackscholes_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma, scheme="euler")
        blackscholes_instance.generate_scenarios(n_paths, n_steps)
        price_vector = np.zeros(n_paths)
        for key in blackscholes_instance.scenarios.keys():
            price_vector[key] = blackscholes_instance.scenarios[key][-1]
        test_result, pvalue = sc.stats.kstest(price_vector, np.random.lognormal(mean=((r-(sigma**2)/2)*t_end), sigma=(sigma ** 2) * t_end, size=n_paths))
        theoretical_values = np.random.lognormal(mean=((r-(sigma**2)/2)*t_end), sigma=(sigma ** 2) * t_end, size=n_paths)
        plt.hist(price_vector, bins=100)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        plt.plot(x, theoretical_values, 'k', linewidth=2)
        plt.show()
        self.assertGreaterEqual(pvalue, 0.05)  # If p-value is lower than 0.05, the distribution hypothesis is rejected


if __name__ == '__main__':
    unittest.main()
