import unittest
from xmlrpc.client import Error

from MarketDataContainer.MkdWrapper import MkdWrapper


class MkdWrapperTest(unittest.TestCase):

    def test_get_current_price(self):
        mkd = MkdWrapper("AAPL")
        #try:
        spot = mkd.load_current_price()
        #except Error:
        #    self.fail("get_current_price() raised an exception")
        self.assertTrue(spot > 0)

    def test_get_implied_volatility(self):
        mkd = MkdWrapper("AAPL")
        try:
            iv = mkd.load_implied_volatility()
        except Error:
            self.fail("get_implied_volatility() raised an exception")
        self.assertTrue(iv > 0)

    def test_edge_cases_interest(self):
        mkd_container = MkdWrapper('^IRX')
        try:
            latest_rate = mkd_container.get_interest_rate()
            self.assertTrue(0 <= latest_rate <= 1)
        except Error:
            self.fail("no result")


if __name__ == '__main__':
    unittest.main()
