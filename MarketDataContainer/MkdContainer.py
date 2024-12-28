from typing import Dict

from MarketDataContainer.MkdWrapper import MkdWrapper


class MkdContainer:
    """
    MKdContainer is a class that gets an underlying list, currency list and fx list that should be loaded.
    In addition, a reference currency yield curve can be set. For this currencies, all common time horizons are loaded.


    """

    def __init__(self):
        self.underlying_list = None
        self.market_data = {}
        self.currency_list = None
        reference_yield_curve_dict = Dict[float, float]
        self.reference_yield_curve: reference_yield_curve_dict = {}
        self.reference_yield_curve_name = None
        self.short_rate = None

    def set_underlying_list(self, underlying_list: list[str]):
        self.underlying_list = underlying_list

    def set_currency_list(self, currency_list: list[str]):
        self.currency_list = currency_list

    def set_reference_curve_name(self, name: str):
        self.reference_yield_curve_name = name

    def get_latest_spot_price(self, company_name: str):
        return self.market_data[company_name]['latest_price']

    def get_today_short_rate(self):
        return self.short_rate

    def get_implied_volatility(self, company_name: str):
        return self.market_data[company_name]['implied_volatility']

    def load(self):
        """
        Load all market data from the source
        """
        # Load reference yield curve:
        if self.reference_yield_curve_name is not None:
            self.reference_yield_curve = MkdWrapper(self.reference_yield_curve_name)
            self.short_rate = self.reference_yield_curve.get_interest_rate()
        # Load all other underlying, e.g. stock prices or fx rates
        if self.underlying_list is not None:
            for underlying_str in self.underlying_list:
                ticker_instance = MkdWrapper(underlying_str)
                mkd_entry = {'latest_price': ticker_instance.load_current_price(),
                             'notional_currency': ticker_instance.get_notional_currency(),
                             'implied_volatility': ticker_instance.load_implied_volatility()}  # Convention: Implied volatility for dt = 7 days
                self.market_data[underlying_str] = mkd_entry
