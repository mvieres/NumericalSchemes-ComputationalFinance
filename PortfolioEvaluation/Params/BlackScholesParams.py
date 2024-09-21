from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams


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
        self.s0 = data.get('s0')
        self.t_start = data.get('t_start')
        self.t_end = data.get('t_end')

    def set_r(self, r):
        self.r = r

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_r(self):
        return self.r

    def get_sigma(self):
        return self.sigma
