from PortfolioEvaluation.Params.AbstractTradeParams import AbstractTradeParams


class StockOptionParams(AbstractTradeParams):

    def __init__(self):
        super().__init__()
        self.category = "stock_option"
        self.type = None
        self.exercise = None
        self.notional_currency = None
        self.strike = None
        self.maturity = None

    def from_dict(self, data):
        super().from_dict(data)
        self.type = data.get('type')
        self.exercise = data.get('exercise')
        self.notional_currency = data.get('notional_currency', "USD")
        self.strike = data.get('strike')
        self.maturity = data.get('maturity')

    def set_type(self, type):
        self.type = type

    def set_exercise(self, exercise):
        self.exercise = exercise

    def set_notional_currency(self, notional_currency):
        self.notional_currency = notional_currency

    def set_strike(self, strike):
        self.strike = strike

    def set_maturity(self, maturity):
        self.maturity = maturity

    def get_type(self):
        return self.type

    def get_exercise(self):
        return self.exercise

    def get_notional_currency(self):
        return self.notional_currency

    def get_strike(self):
        return self.strike

    def get_maturity(self):
        return self.maturity

    def get_category(self):
        return self.category
