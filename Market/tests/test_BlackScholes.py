import unittest
from Market.BlackScholes import BlackScholes


class test_black_scholes(unittest.TestCase):

    def test_init(self):
        blackscholes_instance = BlackScholes(0, 1, 100, 0.01, 0.01, "milstein")
        blackscholes_instance.generateScenarios(4, 1000)
        blackscholes_instance.plot_underlying(1000)


if __name__ == '__main__':
    unittest.main()
