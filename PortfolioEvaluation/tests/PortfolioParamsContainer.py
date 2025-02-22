from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.CIRParams import CIRParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams


class PortfolioParamsContainer:

    @staticmethod
    def portfolio_1():
        portfolio = {
            "name": "some name",
            "trades": [
                {"stock_option": {
                    "id": 1111,
                    "underlying": "AAPL",
                    "type": "call",
                    "exercise": "european",
                    "notional_currency": "USD",
                    "strike": 100,
                    "maturity": "2028-12-10",
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

    @staticmethod
    def portfolio_2():
        portfolio = {
            "name": "some name",
            "trades": [
                {"stock_option": {
                    "id": 1111,
                    "underlying": "AAPL",
                    "type": "call",
                    "exercise": "european",
                    "notional_currency": "USD",
                    "strike": 100,
                    "maturity": "2028-12-10",
                    "quantity": 1
                }
                }
            ],
            "simulation_config": {
                "reference_yield_curve": "USD",
                "use_constant_interest_rate": True,
                "mc_steps": 1000,
                "discretization": 100
            }
        }
        return portfolio

    @staticmethod
    def model_params():
        bs_params = BlackScholesParams()
        bs_params.set_params(0, 1, 1, 0.1, 0.3)
        hs_params = HestonCIRParams()
        hs_params.set_params(0, 1, 100, 0.75, 0.5, 0.5, 0.5, 0.2, 0.3)
        cir_params = CIRParams()
        cir_params.set_params(0, 1, 1, 0.1, 0.1, 0.1)

        return bs_params, hs_params, cir_params
