import unittest

from MarketDataContainer.MkdContainer import MkdContainer


class MkdContainerTest(unittest.TestCase):

    def test_get_short_rate(self):
        mkd_container = MkdContainer()
        mkd_container.set_reference_curve_name('^IRX')
        mkd_container.load()
        self.assertTrue(mkd_container.get_today_short_rate() is not None)

    def test_get_spot_price(self):
        # TODO: there is still a bug
        mkd_container = MkdContainer()
        mkd_container.set_underlying_list(['APPL'])
        mkd_container.load()
        self.assertTrue(mkd_container.get_latest_spot_price('APPL') > 0)


if __name__ == '__main__':
    unittest.main()
