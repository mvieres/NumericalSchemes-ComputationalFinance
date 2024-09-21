from datetime import date

class MkdContainer:
    """

    This has to be implemented. For now, only the get_underlying_today method is needed.

    Today means the date of the simulation, i.s system date.

    """

    def __init__(self, today: date):
        self.today = today
        self.market_data = {}
        supported_company_names = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
        pass

    def get_today_underlying(self, company_name: str):
        return 100

    def get_today_short_rate(self):
        return 0.01

    def load(self):
        """
        Load all market data from the source
        """
        pass