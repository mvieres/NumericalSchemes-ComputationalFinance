from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams


class HestonCIRParams(AbstractModelParams):

    def __init__(self):
        super().__init__()
        self.r = None
        self.sigma = None
        self.v0 = None
        self.kappa = None
        self.theta = None
        self.rho = None

    def from_dict(self, data):
        self.r = data.get('r')
        self.sigma = data.get('sigma')
        self.starting_point = data.get('s0')
        self.v0 = data.get('v0')
        self.t_start = data.get('t_start')
        self.t_end = data.get('t_end')
        self.kappa = data.get('kappa')
        self.theta = data.get('theta')
        self.rho = data.get('rho')

    def set_r(self, r):
        self.r = r

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_v0(self, v0):
        self.v0 = v0

    def set_kappa(self, kappa):
        self.kappa = kappa

    def set_theta(self, theta):
        self.theta = theta

    def set_rho(self, rho):
        self.rho = rho

    def get_r(self):
        return self.r

    def get_sigma(self):
        return self.sigma

    def get_v0(self):
        return self.v0

    def get_kappa(self):
        return self.kappa

    def get_theta(self):
        return self.theta

    def get_rho(self):
        return self.rho
