import unittest

from Pricing.AmercianMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo as lsmc
from Market.BlackScholes import BlackScholes


class MyTestCase(unittest.TestCase):

    def test_lsm_init(self):
        bsInstance = BlackScholes(0, 1, 100, 0.05, 0.2)
        lsmcInstance = lsmc(bsInstance, 1000, 100)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
