import unittest

from PortfolioEvaluation.Params.SimulationKernelParams import SimulationKernelParams
from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams


class SimulationKernelParamsTest(unittest.TestCase):

    def test_functionality(self):
        underlying_params = BlackScholesParams()
        interest_params = TrolleSchwartzParams()
        fx_params = HestonCIRParams()
        sk_params = SimulationKernelParams()

        try:
            sk_params.set_sk_params(1, underlying_params=underlying_params,
                                    interest_rate_params=interest_params, fx_params=fx_params)
            a = sk_params.get(1)
            b = a.get_underlying_params()
            b = a.get_interest_rate_params()
            b = a.get_fx_params()
        except:
            self.fail("Functionality not given")
