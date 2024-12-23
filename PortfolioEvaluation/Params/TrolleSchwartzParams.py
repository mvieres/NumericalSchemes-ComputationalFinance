from PortfolioEvaluation.Params.AbstractModelParams import AbstractModelParams


class TrolleSchwartzParams(AbstractModelParams):
    
    def __init__(self):
        super().__init__()
        self.__alpha_0 = None
        self.__alpha_1 = None
        self.__gamma = None
        self.__kappa = None
        self.__theta = None
        self.__sigma = None
        self.__rho = None
        self.__v0 = None

    def set_alpha_0(self, alpha_0: float):
        self.__alpha_0 = alpha_0

    def set_alpha_1(self, alpha_1: float):
        self.__alpha_1 = alpha_1

    def set_gamma(self, gamma: float):
        self.__gamma = gamma

    def set_kappa(self, kappa: float):
        self.__kappa = kappa

    def set_theta(self, theta: float):
        self.__theta = theta

    def set_sigma(self, sigma: float):
        self.__sigma = sigma

    def set_rho(self, rho: float):
        self.__rho = rho

    def get_alpha_0(self) -> float:
        return self.__alpha_0

    def get_alpha_1(self) -> float:
        return self.__alpha_1

    def get_gamma(self) -> float:
        return self.__gamma

    def get_kappa(self) -> float:
        return self.__kappa

    def get_theta(self) -> float:
        return self.__theta

    def get_sigma(self) -> float:
        return self.__sigma

    def get_rho(self) -> float:
        return self.__rho

    def set_v0(self, v0: float):
        self.__v0 = v0

    def get_v0(self) -> float:
        return self.__v0

    def from_dict(self, params: dict):
        self.set_alpha_0(params['alpha_0'])
        self.set_alpha_1(params['alpha_1'])
        self.set_starting_point(params['f0'])
        self.set_v0(params['v0'])
        self.set_gamma(params['gamma'])
        self.set_kappa(params['kappa'])
        self.set_theta(params['theta'])
        self.set_sigma(params['sigma'])
        self.set_rho(params['rho'])