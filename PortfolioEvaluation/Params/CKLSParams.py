from PortfolioEvaluation.Params.CIRParams import CIRParams


class CKLSParams(CIRParams):

    def __init__(self):
        super().__init__()
        self.gamma = None

    def from_dict(self, data):
        super().from_dict(data)
        self.set_gamma(data.get('gamma'))

    def set_gamma(self, gamma):
        self.gamma = gamma

    def get_gamma(self):
        return self.gamma