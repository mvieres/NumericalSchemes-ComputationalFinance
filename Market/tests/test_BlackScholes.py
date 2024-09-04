import unittest
from Market.BlackScholes import BlackScholes


class BlackScholesTest(unittest.TestCase):

    def test_init(self):
        blackscholes_instance = BlackScholes(0, 10, 100, 0.1, 0.5, "milstein")
        blackscholes_instance.generateScenarios(4, 1000)
        blackscholes_instance.plot_underlying()


if __name__ == '__main__':
    unittest.main()
