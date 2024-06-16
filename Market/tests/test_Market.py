import unittest
import Market.Market as M
import matplotlib.pyplot as plt


class MarketTest(unittest.TestCase):

    def test_BSModelSolutionEuler(self):
        BlackScholesInstance = M.BlackScholes(0, 1, 100, 0.01, 0.01, "milstein")
        solutionPath = BlackScholesInstance.computeSolutionPath(1000)
        plt.plot(BlackScholesInstance.timeGridInstance.getTimeGrid(1000), solutionPath)
        plt.show()
        self.assertEqual(solutionPath.shape, (3, 1))


if __name__ == '__main__':
    unittest.main()
