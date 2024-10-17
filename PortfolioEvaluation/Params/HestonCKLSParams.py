from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams


class HestonCKLSParams(HestonCIRParams):

    def __init__(self):
        super().__init__()
        self.gamma = None

    def from_dict(self, data):
        super().from_dict(data)
        self.gamma = data.get('gamma')

    def set_gamma(self, gamma):
        self.gamma = gamma

    def get_gamma(self):
        return self.gamma