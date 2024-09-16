import unittest
import matplotlib.pyplot as plt

import NumericalSchemes.SdeSolver as solver
import NumericalSchemes.TimeGrid as timegrid


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


if __name__ == '__main__':
    unittest.main()
