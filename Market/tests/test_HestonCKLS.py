import unittest
import matplotlib.pyplot as plt

from Market.HestonCKLS import HestonCKLS


class HestonCKLSTest(unittest.TestCase):

    def test_functionality(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 6
        r = 0.1
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        gamma = 0.6
        hestonckls_instance = HestonCKLS(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, gamma, "absolute_euler")
        try:
            hestonckls_instance.generate_scenarios(4, 10)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    def test_plot(self):
        t_start = 0
        t_end = 1
        s0 = 100
        v0 = 6
        r = 0.1
        kappa = 0.1
        theta = 0.2
        sigma = 0.1
        rho = 0.01
        gamma = 0.6
        hestonckls_instance = HestonCKLS(t_start, t_end, s0, v0, r, kappa, theta, sigma, rho, gamma, "absolute_euler")
        hestonckls_instance.generate_scenarios(4, 1000)
        plt.plot(hestonckls_instance.time_grid_instance.get_time_grid(1000), hestonckls_instance.underlying[1][:, 0])
        plt.plot(hestonckls_instance.time_grid_instance.get_time_grid(1000), hestonckls_instance.underlying[1][:, 1])
        plt.legend(["Spot", "Volatility"])
        plt.xlabel("Time")
        plt.ylabel("Price / Volatility")
        plt.show()

if __name__ == '__main__':
    unittest.main()
