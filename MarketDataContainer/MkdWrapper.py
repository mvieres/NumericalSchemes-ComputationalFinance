import yfinance as yf


class MkdWrapper:
    """
    TODO: make sense of this class
    """

    def __init__(self, company_name: str):
        self.ticker_instance = yf.Ticker(company_name)

    def get_call_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).calls['lastPrice']

    def get_put_prices(self, expiration_date: str):
        return self.ticker_instance.option_chain(expiration_date).puts['lastPrice']
