import unittest

from Market.Heston import Heston


class HestonTest(unittest.TestCase):

    def test_init(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 1
        mue = 0.01
        r = 0
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        scheme = "euler"
        heston_instance = Heston(t_start, t_end, s0, v0, mue, r, kappa, theta, sigma, rho, scheme)
        heston_instance.generate_scenarios(4, 1000)
        heston_instance.plot_underlying()
        pass

    def test_functionality(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 1
        mue = 0.01
        r = 0
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        scheme = "euler"
        heston_instance = Heston(t_start, t_end, s0, v0, mue, r, kappa, theta, sigma, rho, scheme)
        try:
            heston_instance.generate_scenarios(4, 10)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error: {e} was raised")

    def test_cond_distribution(self):
        # TODO: Test conditional distribution of CIR process
        pass


if __name__ == '__main__':
    unittest.main()
