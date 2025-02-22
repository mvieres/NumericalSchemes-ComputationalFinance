import numpy as np

from Market.BlackScholes import BlackScholes
from Market.HestonCIR import HestonCIR
from Market.HestonCKLS import HestonCKLS
from Market.CIR import CIR
from Market.CKLS import CKLS
from Pricing.MonteCarloUtility import MonteCarloUtility


class StandardMonteCarlo(MonteCarloUtility):

    def __init__(self, underlying_instance: BlackScholes or HestonCIR or HestonCKLS or CIR or CKLS,
                 payoff: str, payoff_params: dict, n_paths: int, n_steps: int,
                 discount_curve: CIR or CKLS or float, fx_curve=None):
        super().__init__(payoff, payoff_params, underlying_instance, n_paths, n_steps, discount_curve, fx_curve)

    def compute_option_price(self):
        """

        """
        value_list = []
        scenario_keys = self.underlying_instance.scenarios.keys()

        for scenario in scenario_keys:
            underlying_price = self.underlying_instance.get_scenario(scenario)
            value = self.payoff.eval(underlying_price)
            if self.fx_curve is not None:
                value *= self.fx_curve.get_scenario(scenario)[-1]
            if self.discount_curve is not None:
                discount_factor = np.exp(-np.trapz(self.discount_curve.get_scenario(scenario), self.grid))
            else:
                discount_factor = self.discount_factor  # constant discount factor
            if discount_factor <= 0.0:
                raise ValueError("Discount factor must be positive")
            value *= discount_factor
            value_list.append(value)
        return sum(value_list) / len(value_list)
