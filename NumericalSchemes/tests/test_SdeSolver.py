import unittest

import NumericalSchemes.SdeSolver as solver
import NumericalSchemes.TimeGrid as timegrid


class SdeSolverTest(unittest.TestCase):

    def test_EulerMultiDimensional(self):
        """
        dX_1 = -cos(X_2)
        dX_2 = sin(X_1)
        @return:
        """

    def test_EulerOneDimensional(self):
        """
        Testing black scholes: dX_t = mue*X dt + sigma*X dW_t
        """
        drift = lambda t, x: 1 * x
        diffusion = lambda t, x: 0.1 * x
        timeGridInstance = timegrid.TimeGrid(0, 1)
        solution = solver.SdeSolver.euler(timeGridInstance, 100, 0, drift, diffusion)
        self.assertEqual(solution.shape(), (1,))


if __name__ == '__main__':
    unittest.main()
