import unittest
import Market.BlackScholes as BlackScholes
import matplotlib.pyplot as plt


class test_Market(unittest.TestCase):

    def test_BSModelSolutionEuler(self):
        BlackScholesInstance = BlackScholes.BlackScholes(0, 1, 100, 0.01, 0.01, "milstein")
        solutionPath = BlackScholesInstance.compute_solution_path(1000)
        plt.plot(BlackScholesInstance.timeGridInstance.get_time_grid(1000), solutionPath)
        plt.show()
        self.assertEqual(solutionPath.shape, (3, 1))
