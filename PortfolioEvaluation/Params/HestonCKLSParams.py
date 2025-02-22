from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from Utility.ModelEnum import ModelEnum as me


class HestonCKLSParams(HestonCIRParams):

    def __init__(self):
        super().__init__()
        self.gamma = None

    def get_model_name(self):
        return me.HestonCKLS.value

    def from_dict(self, data):
        super().from_dict(data)
        self.gamma = data.get('gamma')

    def set_gamma(self, gamma):
        self.gamma = gamma

    def get_gamma(self):
        return self.gamma