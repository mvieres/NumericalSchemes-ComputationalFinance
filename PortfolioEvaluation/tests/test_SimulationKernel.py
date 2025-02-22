import unittest

from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.CIRParams import CIRParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.SimulationKernelParams import SimulationKernelParams
from PortfolioEvaluation.SimulationKernel import SimulationKernel


class SimulationKernelTest(unittest.TestCase):

    def test_functionality(self):
        # TODO:
        # get sk params
        sk_params = self.setup_test()
        sk_instance = SimulationKernel(sk_params.get_general_sim_params())
        sk_instance.set_job_request(sk_params.get(1111))
        sk_instance.run_new()
        self.assertEquals(True, False)

    def setup_test(self):
        sk_params = SimulationKernelParams()
        sk_params.pull_from_input(self.__test_portfolio_data())
        bs_params, _, cir_params = self.__get_model_params()
        sk_params.set_sk_params(1111, underlying_params=bs_params, interest_rate_params=cir_params, fx_params=None)
        return sk_params

    def __get_model_params(self):
        bs_params = BlackScholesParams()
        bs_params.set_params(0, 1, 1, 0.1, 0.3)
        hs_params = HestonCIRParams()
        hs_params.set_params(0, 1, 100, 0.75, 0.5, 0.5, 0.5, 0.2, 0.3)
        cir_params = CIRParams()
        cir_params.set_params(0, 1, 1, 0.1, 0.1, 0.1)

        return bs_params, hs_params, cir_params

    def __test_portfolio_data(self):
        portfolio ={
              "name": "some name",
              "trades":[
                {"stock_option": {
                    "id": 1111,
                    "underlying": "AAPL",
                    "type": "call",
                    "exercise": "european",
                    "notional_currency": "USD",
                    "strike": 100,
                    "maturity": "2024-12-10",
                    "quantity": 1
                    }
                }
              ],
              "simulation_config": {
                "reference_yield_curve": "USD",
                "use_constant_interest_rate": False,
                "mc_steps": 1000,
                "discretization": 100
              }
            }
        return portfolio


if __name__ == '__main__':
    unittest.main()
