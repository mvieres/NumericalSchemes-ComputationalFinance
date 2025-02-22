import numpy as np

from Market.BlackScholes import BlackScholes
from Market.HestonCIR import HestonCIR
from Market.HestonCKLS import HestonCKLS
from Market.CIR import CIR
from Market.CKLS import CKLS
from Utility.Payoff import Payoff


class MonteCarloUtility:

    def __init__(self, payoff: str, payoff_params: dict,
                 underlying_instance: BlackScholes or HestonCIR or HestonCKLS or CIR or CKLS, n_paths: int,
                 n_steps: int, discount_curve: CIR or CKLS or float, fx_curve=None):
        self.underlying_instance = underlying_instance
        self.grid = underlying_instance.time_grid_instance.get_time_grid(n_steps)
        if isinstance(discount_curve, float):
            self.use_constant_discount = True
            self.discount_factor = np.exp(-discount_curve*(self.grid[-1] - self.grid[0]))
        self.discount_curve = discount_curve
        self.fx_curve = fx_curve
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.__check_for_market_scenarios()
        self.payoff = Payoff(name=payoff, params=payoff_params)  # This is the instance to evaluate the payoff
        self.exercise_type = self.payoff.get_exercise_type()

    def __check_for_market_scenarios(self):
        if len(self.underlying_instance.get_scenarios().keys()) == 0:
            self.underlying_instance.generate_scenarios(self.n_paths, self.n_steps)
        if not isinstance(self.discount_curve, float):
            if len(self.discount_curve.get_scenarios().keys()) == 0:
                self.discount_curve.generate_scenarios(self.n_paths, self.n_steps)
        if self.fx_curve is not None:
            if len(self.fx_curve.get_scenarios().keys()) == 0:
                self.fx_curve.generate_scenarios(self.n_paths, self.n_steps)

    @staticmethod
    def validate_instance(instance):
        assert isinstance(instance, (BlackScholes, HestonCIR, HestonCKLS, CIR, CKLS)), "Invalid instance type"