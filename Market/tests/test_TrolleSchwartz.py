import unittest

from Market.TrolleSchwartz import TrolleSchwartz


class TrolleSchwartzTest(unittest.TestCase):

    def test_functionality(self):
        t_start = 0
        t_end = 1
        r = 0.1
        alpha_0 = 0.2
        alpha_1 = 0.3
        gamma = 0.4
        kappa = 0.5
        theta = 0.6
        sigma = 0.7
        rho = -0.5
        n_steps = 1000
        n_paths = 3
        trolle_schwartz = TrolleSchwartz(t_start, t_end, r, alpha_0, alpha_1,
                                         gamma, kappa, theta, sigma, rho, 'absolute_euler')
        try:
            trolle_schwartz.generate_scenarios(n_paths=n_paths, n_steps=n_steps)
            trolle_schwartz.plot_underlying()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Error {e} occured during computation of solution path")

    @unittest.skip("For visual inspection only")
    def test_plot(self):
        t_start = 0
        t_end = 1
        r = 0.1
        alpha_0 = 0.2
        alpha_1 = 0.3
        gamma = 0.4
        kappa = 0.5
        theta = 0.6
        sigma = 0.7
        rho = -0.5
        n_steps = 1000
        n_paths = 3
        trolle_schwartz = TrolleSchwartz(t_start, t_end, r, alpha_0, alpha_1,
                                         gamma, kappa, theta, sigma, rho, 'absolute_euler')
        trolle_schwartz.generate_scenarios(n_paths=n_paths, n_steps=n_steps)
        trolle_schwartz.plot_underlying()

if __name__ == '__main__':
    unittest.main()
