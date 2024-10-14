import unittest

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
from Market.BlackScholes import BlackScholes


class BlackScholesTest(unittest.TestCase):

    #@unittest.skip("Plot for visual inspection")
    def test_init(self):
        blackscholes_instance = BlackScholes(0, 1000, 100, 0.01, 0.0001, "milstein")
        blackscholes_instance.generate_scenarios(1, 1000)
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
        # TODO: this should work
        t_start = 0
        t_end = 1
        s0 = 100
        r = 0.05
        sigma = 0.2
        n_steps = 1000
        n_paths = 1000
        blackscholes_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma, scheme="euler")
        blackscholes_instance.generate_scenarios(n_paths, n_steps)
        price_vector = np.zeros(n_paths)
        for key in blackscholes_instance.scenarios.keys():
            price_vector[key] = blackscholes_instance.scenarios[key][-1]
        test_result, pvalue = sc.stats.kstest(price_vector, np.random.lognormal(mean=((r-(sigma**2)/2)*t_end), sigma=(sigma ** 2) * t_end, size=n_paths))
        #theoretical_values = np.random.lognormal(mean=((r-(sigma**2)/2)*t_end), sigma=(sigma ** 2) * t_end, size=n_paths)
        #plt.hist(price_vector, bins=400)
        #xmin, xmax = plt.xlim()
        #x = np.linspace(xmin, xmax, n_paths)
        #plt.plot(x, theoretical_values, 'k', linewidth=2)
        #plt.show()
        self.assertGreaterEqual(pvalue, 0.05)  # If p-value is lower than 0.05, the distribution hypothesis is rejected

    #@unittest.skip("Plot for visual inspection")
    def test_sample_variance_equals_sigma2(self):
        """
            This function as an example that sample variance is not equal to sigma^2
        """
        t_start = 0
        t_end = 1
        s0 = 100
        r = 0.05
        sigma = 0.2
        n_steps = 1000
        n_paths = 1
        bs_instance = BlackScholes(t_start, t_end, s0, r, sigma, "milstein")
        bs_instance.generate_scenarios_exact(n_paths, n_steps)
        bs_instance.plot_underlying()
        print(bs_instance.scenarios[0])
        print(f"Sample variance: {np.var(bs_instance.scenarios[0], ddof=1)}")
        print(f"Sample mean: {np.mean(bs_instance.scenarios[0])}")
        print(f"Sigma squared: {sigma**2}")


if __name__ == '__main__':
    unittest.main()
