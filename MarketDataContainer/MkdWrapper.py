import numpy as np
import yfinance as yf


class MkdWrapper:
    """
    TODO: make sense of this class
    """

    def __init__(self, company_name: str):
        self.ticker_instance = yf.Ticker(company_name)
        self.info = self.ticker_instance.info
        self.notional_currency = self.info['currency']
        self.yield_cruves_list = ['^IRX']

    def get_notional_currency(self):
        return self.notional_currency

    def get_current_price(self):
        """
        Dirty solution to get latest market price TODO: improve this
        """
        if self.ticker_instance.info['previousClose'] is not None:
            if self.ticker_instance.info.get('symbol') in self.yield_cruves_list:
                self.ticker_instance.info['open'] = self.ticker_instance.info.get('open') / 100
            return self.ticker_instance.info.get('open')
        else:
            if self.ticker_instance.info.get('symbol') in self.yield_cruves_list:
                self.ticker_instance.info['previousClose'] = self.ticker_instance.info.get('previousClose') / 100
            return self.ticker_instance.info['previousClose']


    def get_call_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).calls['lastPrice']

    def get_put_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).puts['lastPrice']

    def get_interest_rate(self):
        assert self.ticker_instance.info.get('symbol') in self.yield_cruves_list, "Method call only meaningful for yield curves"
        return self.get_current_price()