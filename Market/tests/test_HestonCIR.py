import unittest

import matplotlib.pyplot as plt

from Market.HestonCIR import HestonCIR


class HestonCIRTest(unittest.TestCase):

    @unittest.skip("Plot for visual inspection")
    def test_init(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 1
        r = 0.1
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        scheme = "absolute_euler"
        heston_instance = HestonCIR(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, scheme)
        heston_instance.generate_scenarios(1, 1000)
        heston_instance.plot_underlying()

    @unittest.skip("Plot for visual inspection")
    def test_compute_solution_old(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 10
        r = 0.1
        kappa = 1
        theta = 10
        sigma = 2
        rho = 0.2
        scheme = "absolute_euler"
        heston_instance = HestonCIR(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, scheme)
        heston_instance.scenarios[1] = heston_instance.compute_solution_path_old(1000)
        plt.plot(heston_instance.time_grid_instance.get_time_grid(1000), heston_instance.scenarios[1][:, 0])
        plt.plot(heston_instance.time_grid_instance.get_time_grid(1000), heston_instance.scenarios[1][:, 1])
        plt.legend(["Spot", "Volatility"])
        plt.xlabel("Time")
        plt.ylabel("Price / Volatility")
        plt.show()

    def test_functionality(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 1
        r = 0
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        scheme = "absolute_euler"
        heston_instance = HestonCIR(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, scheme)
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
