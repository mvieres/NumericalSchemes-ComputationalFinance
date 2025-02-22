from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams
from Utility.ModelEnum import ModelEnum as me


class BlackScholesParams(AbstractModelParams):
    """
    This class save all important parameters for simulation of a given trade; hence, parameters needed by
    classes from the module NumercialSchemes should be included here.
    """

    def __init__(self):
        super().__init__()
        self.r = None
        self.sigma = None

    def from_dict(self, data):
        # This classes should not have a from dict command (I guess)
        self.r = data.get('r')
        self.sigma = data.get('sigma')
        self.starting_point = data.get('s0')
        self.t_start = data.get('t_start')
        self.t_end = data.get('t_end')

    def get_model_name(self):
        return me.BlackScholes.value

    def set_r(self, r):
        self.r = r

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_r(self):
        return self.r

    def get_sigma(self):
        return self.sigma

    def set_params(self, t_start, t_end, starting_point, r, sigma):
        self.t_start = t_start
        self.t_end = t_end
        self.starting_point = starting_point
        self.r = r
        self.sigma = sigma
