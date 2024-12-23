from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams


class CIRParams(AbstractModelParams):

    def __init__(self):
        super().__init__()
        self.theta = None
        self.kappa = None
        self.sigma = None

    def from_dict(self, data):
        self.set_theta(data.get('theta'))
        self.set_kappa(data.get('kappa'))
        self.set_sigma(data.get('sigma'))
        self.set_starting_point(data.get('s0'))
        self.set_t_start(data.get('t_start'))
        self.set_t_end(data.get('t_end'))

    def set_theta(self, theta):
        self.theta = theta

    def set_kappa(self, kappa):
        self.kappa = kappa

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_theta(self):
        return self.theta

    def get_kappa(self):
        return self.kappa

    def get_sigma(self):
        return self.sigma
