import unittest
import matplotlib.pyplot as plt
import numpy as np

import NumericalSchemes.SdeSolver as solver
import NumericalSchemes.TimeGrid as timegrid
from NumericalSchemes.TimeGrid import TimeGrid


class SdeSolverTest(unittest.TestCase):

    def test_EulerMultiDimensional(self):
        """
        dX_1 = t*X_1 dt + X_2 dW_1 + X_2^2 dW_2
        dX_2 = X_2 dt + X_2 dW_2
        TODO: check this with a known multidimensional distribution of an sde -> multidimensional black scholes with correlation
        @return:
        """
        drift = {1: lambda t, x: t*x[0], 2: lambda t, x: x[1]}
        diffusion = {1: {1: lambda t, x: x[1], 2: lambda t, x: x[1]**2}, 2: {2: lambda t, x: x[1]}}
        time_grid_instance = timegrid.TimeGrid(0, 1)
        solution_instance = solver.SdeSolver(time_grid_instance, drift, diffusion, [1, 1])
        solution = solution_instance.euler(100)
        plt.plot(time_grid_instance.get_time_grid(100), solution[:, 0])
        plt.plot(time_grid_instance.get_time_grid(100), solution[:, 1])
        plt.show()

    def test_EulerOneDimensional_1(self):
        """
        Testing black scholes: dX_t = mue*X dt + sigma*X dW_t (autonomous sde)
        """
        drift = lambda t, x: 1 * x
        diffusion = lambda t, x: 0.1 * x
        timeGridInstance = timegrid.TimeGrid(0, 1)
        solution_instance = solver.SdeSolver(timeGridInstance, drift, diffusion, 1)
        solution = solution_instance.euler(100)
        plt.plot(solution)
        plt.show()
        self.assertEqual(solution.shape(), (1,))

    def test_EulerOneDimensional_2(self):
        """
        Testing non-autonomous sde: dX_t = ? dt + ? dW_t

        """

    def test_implicit_euler(self):
        time_grid = TimeGrid(0, 1)
        drift = lambda t, x: 4 * x
        diffusion = lambda t, x: 0.001
        starting_point = 1
        real_solution = lambda t: np.exp(4 * t)
        n_steps = 1000
        sde_solver = solver.SdeSolver(time_grid, drift, diffusion, starting_point)
        sol = sde_solver.drift_implicit_euler(n_steps)
        r_sol = real_solution(time_grid.get_time_grid(n_steps))
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], r_sol[i], delta=0.5)
        #plt.plot(time_grid.get_time_grid(n_steps), sol, label='implicit')
        #plt.plot(time_grid.get_time_grid(n_steps), r_sol, label='real')
        #plt.legend()
        #plt.show()


if __name__ == '__main__':
    unittest.main()
