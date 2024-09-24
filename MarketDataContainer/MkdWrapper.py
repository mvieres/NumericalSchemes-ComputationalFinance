from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd

class MkdWrapper:
    """
    TODO: make sense of this class
    """

    def __init__(self, underlying_name: str):
        self.underlying_name = underlying_name
        self.ticker_instance = yf.Ticker(underlying_name)
        self.info = self.ticker_instance.info
        self.notional_currency = self.info['currency']
        self.yield_cruves_list = ['^IRX']

    def get_notional_currency(self):
        return self.notional_currency

    def load_current_price(self):
        """
        Dirty solution to get latest market price TODO: improve this
        """
        if 'open' in self.ticker_instance.info:
            if self.ticker_instance.info.get('symbol') in self.yield_cruves_list:
                self.ticker_instance.info['open'] = self.ticker_instance.info.get('open') / 100
            return self.ticker_instance.info.get('open')
        else:
            if self.ticker_instance.info.get('symbol') in self.yield_cruves_list:
                self.ticker_instance.info['previousClose'] = self.ticker_instance.info.get('previousClose') / 100
            return self.ticker_instance.info['previousClose']

    def load_implied_volatility(self, expiration_date = None):
        if self.underlying_name in self.yield_cruves_list:  # Not possible to load implied volatility for yield curves at this point
            raise ValueError("Implied volatility not available for yield curves, do not try to load it")
        if expiration_date is None:
            expiration_date = self.__next_business_day(datetime.today() + timedelta(weeks=1)).strftime('%Y-%m-%d')
        assert expiration_date is not None, "Expiration date is not set"
        if expiration_date not in self.ticker_instance.options:
            expiration_date = self.ticker_instance.options[-1]  # If expiration date is not available, take the last one that is available
        options = self.ticker_instance.option_chain(expiration_date)
        calls = options.calls
        spot_price = self.load_current_price()
        closest_call = calls.iloc[(calls['strike'] - spot_price).abs().argsort()[:1]]
        return closest_call['impliedVolatility'].values[0]

    def get_call_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).calls['lastPrice']

    def get_put_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).puts['lastPrice']

    def get_interest_rate(self):
        assert self.ticker_instance.info.get('symbol') in self.yield_cruves_list,\
            "Method call only meaningful for yield curves"
        return self.load_current_price()

    @staticmethod
    def __is_business_day(date):
        return bool(len(pd.bdate_range(date, date)))

    @staticmethod
    def __next_business_day(date):
        next_day = date + timedelta(days=1)
        while not bool(len(pd.bdate_range(next_day, next_day))):
            next_day += timedelta(days=1)
        return next_day