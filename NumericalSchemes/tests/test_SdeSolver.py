import unittest
import matplotlib.pyplot as plt
import numpy as np

from NumericalSchemes.SdeSolver import SdeSolver
from NumericalSchemes.TimeGrid import TimeGrid


class SdeSolverTest(unittest.TestCase):

    @unittest.skip("Plot for visual inspection")
    def test_EulerMultiDimensional(self):
        """
        dX_1 = t*X_1 dt + X_2 dW_1 + X_2^2 dW_2
        dX_2 = X_2 dt + X_2 dW_2
        TODO: check this with a known multidimensional distribution of an sde -> multidimensional black scholes with correlation
        @return:
        """
        drift = {1: lambda t, x: t*x[0], 2: lambda t, x: x[1]}
        diffusion = {1: {1: lambda t, x: x[1], 2: lambda t, x: x[1]**2}, 2: {2: lambda t, x: x[1]}}
        time_grid_instance = TimeGrid(0, 1)
        solution_instance = SdeSolver(time_grid_instance, drift, diffusion, [1, 1])
        solution = solution_instance.euler(100)
        plt.plot(time_grid_instance.get_time_grid(100), solution[:, 0])
        plt.plot(time_grid_instance.get_time_grid(100), solution[:, 1])
        plt.show()

    @unittest.skip("Plot for visual inspection")
    def test_EulerOneDimensional_1(self):
        """
        Testing black scholes: dX_t = mue*X dt + sigma*X dW_t (autonomous sde)
        """
        drift = lambda t, x: 1 * x
        diffusion = lambda t, x: 0.1 * x
        timeGridInstance = TimeGrid(0, 1)
        solution_instance = SdeSolver(timeGridInstance, drift, diffusion, 1)
        solution = solution_instance.euler(100)
        plt.plot(solution)
        plt.show()
        self.assertEqual(solution.shape(), (1,))

    def test_EulerOneDimensional_2(self):
        """
        Testing non-autonomous sde: dX_t = ? dt + ? dW_t

        """

    def test_implicit_euler(self):
        """
        Idea: Test exponential function f_prime = 4*f + some noise. Since noise (diffusion) is close to zero,
        the solution should be near the deterministic solution f(t) = exp(4*t)
        """
        time_grid = TimeGrid(0, 1)
        drift = lambda t, x: 4 * x
        diffusion = lambda t, x: 0.001
        starting_point = 1
        real_solution = lambda t: np.exp(4 * t)
        n_steps = 1000
        sde_solver = SdeSolver(time_grid, drift, diffusion, starting_point)
        sol = sde_solver.drift_implicit_euler(n_steps)
        r_sol = real_solution(time_grid.get_time_grid(n_steps))
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], r_sol[i], delta=0.5)
        #plt.plot(time_grid.get_time_grid(n_steps), sol, label='implicit')
        #plt.plot(time_grid.get_time_grid(n_steps), r_sol, label='real')
        #plt.legend()
        #plt.show()

    @unittest.skip("Plot for visual inspection")
    def test_cir_absolute_euler(self):
        time_grid = TimeGrid(0, 1)
        kappa = 0.1
        theta = 1
        sigma = 0.5
        drift = lambda t, x: kappa*(theta - x)
        diffusion = lambda t, x: sigma*np.sqrt(x)
        starting_point = 1
        n_steps = 1000
        sde_solver = SdeSolver(time_grid, drift, diffusion, starting_point)
        sol = sde_solver.absolute_euler(n_steps)
        plt.plot(time_grid.get_time_grid(n_steps), sol)
        plt.show()
        self.assertTrue(True)

    def test_cir_absolute_euler_cond_mean_var(self):
        time_grid = TimeGrid(0, 1)
        kappa = 0.1
        theta = 1
        sigma = 0.5
        drift = lambda t, x: kappa * (theta - x)
        diffusion = lambda t, x: sigma * np.sqrt(x)
        starting_point = 1
        n_steps = 100
        n_samples = 100000
        sde_solver = SdeSolver(time_grid, drift, diffusion, starting_point)
        sol = np.zeros((n_samples, n_steps))
        for i in range(n_samples):
            sol[i] = sde_solver.absolute_euler(n_steps)
        # conditional mean and variance based on the t_0 value
        theoeretical_mean = theta + (starting_point - theta) * np.exp(-kappa*1)
        theoeretical_var = ((sigma**2)*np.exp(-kappa) / kappa)*(1-np.exp(-kappa)) + ((theta*sigma**2)/(2*kappa))*(1-np.exp(-kappa))**2
        empirical_mean = np.mean(sol[:, -1])
        empirical_var = np.var(sol[:, -1])
        self.assertAlmostEqual(theoeretical_mean, empirical_mean, delta=0.01)
        self.assertAlmostEqual(theoeretical_var, empirical_var, delta=0.01)

if __name__ == '__main__':
    unittest.main()
