from PortfolioEvaluation.Params.CIRParams import CIRParams
from Utility.ModelEnum import ModelEnum as me

class CKLSParams(CIRParams):

    def __init__(self):
        super().__init__()
        self.gamma = None

    def get_model_name(self):
        return me.CKLS.value

    def from_dict(self, data):
        super().from_dict(data)
        self.set_gamma(data.get('gamma'))

    def set_gamma(self, gamma):
        self.gamma = gamma

    def get_gamma(self):
        return self.gamma