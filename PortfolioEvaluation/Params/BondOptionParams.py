from PortfolioEvaluation.Params.AbstractTradeParams import AbstractTradeParams


class BondOptionParams(AbstractTradeParams):

    def __init__(self):
        super().__init__()
        self.category = "bond_option"

    def from_dict(self, data):
        pass

    def get_category(self):
        return self.category
