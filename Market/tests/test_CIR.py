import unittest
import numpy as np

from Market.CIR import CIR


class CIRTest(unittest.TestCase):

    def test_functionality(self):
        t_start = 0
        t_end = 1
        x0 = 1
        theta = 1
        kappa = 0.1
        sigma = 0.5
        scheme = "absolute_euler"
        cir_instance = CIR(t_start, t_end, x0, theta, kappa, sigma, scheme)
        try:
            cir_instance.generate_scenarios(4, 10)
        except Exception as e:
            self.fail(f"Failed with exception {e}")

    def test_cond_mean_var(self):
        kappa = 0.1
        theta = 1
        sigma = 0.5
        starting_point = 1
        n_steps = 100
        n_samples = 100000
        cir_instance = CIR(t_start=0, t_end=1, x0=starting_point, theta=theta, kappa=kappa, sigma=sigma, scheme='absolute_euler')
        cir_instance.generate_scenarios(n_samples, n_steps)
        sol = cir_instance.scenarios
        theoeretical_mean = theta + (starting_point - theta) * np.exp(-kappa * 1)
        theoeretical_var = ((sigma ** 2) * np.exp(-kappa) / kappa) * (1 - np.exp(-kappa)) + (
                    (theta * sigma ** 2) / (2 * kappa)) * (1 - np.exp(-kappa)) ** 2
        empirical_mean = np.mean([sol[i][-1] for i in sol.keys()])
        empirical_var = np.var([sol[i][-1] for i in sol.keys()])
        self.assertAlmostEqual(theoeretical_mean, empirical_mean, delta=0.01)
        self.assertAlmostEqual(theoeretical_var, empirical_var, delta=0.01)
