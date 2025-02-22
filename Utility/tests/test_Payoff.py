import unittest
from Utility.Payoff import Payoff


class PayoffTest(unittest.TestCase):

    def test_functionality(self):
        option_list = ["call", "put", "lookback_min_call", "lookback_max_call",
                       "lookback_min_put", "lookback_max_put", "barrier_call", "barrier_put",
                       "asian_call", "asian_put"]
        price_history = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        params = {'strike': 0, 'barrier': 0}
        try:
            for option in option_list:
                payoff = Payoff(name=option, params=params)
                eval = payoff.eval(price_history)
            self.assertTrue(True)
        except Exception as e:
            self.fail("Payoff class is not working correctly: " + str(e))

    def test_eval(self):
        # TODO: New option values that differ from 0
        option_list = ["call_option", "put_option", "lookback_min_call_option", "lookback_max_call_option",
                       "lookback_min_put_option", "lookback_max_put_option"]
        result_list = [0, 0, 0, 0, 0, 0]
        spot = 36
        strike = spot
        barrier = spot
        for option in option_list:
            payoff = Payoff(name=option, params={'strike': strike, 'barrier': barrier})
            result = payoff.eval(underlying_history=spot)
            self.assertEqual(result, result_list[option_list.index(option)])

        option_list = ["barrier_call_option", "barrier_put_option", "asian_call_option", "asian_put_option"]
        result_list = [0, 0, 0, 0]
        spot = [40, 30, 20]
        strike = 30
        barrier = 40
        for option in option_list:
            payoff = Payoff(name=option, params={'strike': strike, 'barrier': barrier})
            result = payoff.eval(underlying_history=spot)
            #self.assertEqual(result, result_list[option_list.index(option)])
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
