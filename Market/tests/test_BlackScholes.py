import unittest
from Market.BlackScholes import BlackScholes


class BlackScholesTest(unittest.TestCase):

    def test_init(self):
        blackscholes_instance = BlackScholes(0, 5, 100, 0.01, 0.5, "milstein")
        blackscholes_instance.generate_scenarios(8, 1000)
        blackscholes_instance.plot_underlying()


if __name__ == '__main__':
    unittest.main()
