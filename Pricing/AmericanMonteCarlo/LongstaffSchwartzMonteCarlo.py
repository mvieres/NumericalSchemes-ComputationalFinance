import numpy as np
import scipy.special as ss

from Market.BlackScholes import BlackScholes
from Market.HestonCIR import HestonCIR
from Market.HestonCKLS import HestonCKLS
from Market.CIR import CIR
from Market.CKLS import CKLS
from Pricing.MonteCarloUtility import MonteCarloUtility


class LongstaffSchwartzMonteCarlo(MonteCarloUtility):
    """
    AMC for american Put and Call Options .
    """

    def __init__(self, payoff: str, payoff_params: dict,
                 underlying_instance: BlackScholes or HestonCIR or HestonCKLS or CIR or CKLS, n_paths: int,
                 n_steps: int, discount_curve: CIR or CKLS or float, fx_curve=None):
        super().__init__(payoff, payoff_params, underlying_instance, n_paths, n_steps, discount_curve, fx_curve)
        self.discount_curve = discount_curve
        self.time_grid = underlying_instance.time_grid_instance.get_time_grid(self.n_steps)
        # AMC specific
        self.default_type = "polynomial"
        self.__regression_types = {
            "legendre": np.polynomial.legendre.legfit,
            "laguerre": np.polynomial.laguerre.lagfit,
            "polynomial": np.polyfit
        }
        self.__evaluation = {
            "legendre": ss.eval_legendre,
            "laguerre": ss.eval_laguerre,
            "polynomial": np.polyval
        }
        self.degree = 3
        # Output
        self.var_mc = None
        self.value = None
        self.value_0 = None
        self.rmse = None
        self.v0_var = None

    def set_degree(self, degree: int) -> None:
        self.degree = degree

    def set_regression_type(self, regressiontype: str):
        self.default_type = regressiontype

    def generate_samples(self):
        self.underlying_instance.compute_solution_path(self.n_steps)

    def compute_option_price(self, return_type=False) -> np.array:
        asset_price = np.zeros(shape=(self.n_paths, self.n_steps))
        # TODO: Adjust this to the new payoff structure
        for key in self.underlying_instance.scenarios.keys():
            if self.underlying_instance.dimension == 2:
                asset_price[key] = self.underlying_instance.scenarios[key][:, 0]
            else:
                asset_price[key] = self.underlying_instance.scenarios[key]
        value = np.zeros_like(asset_price)
        for path in range(self.n_paths):
            value[path, -1] = self.payoff.eval(asset_price[path, :])



        for time_index in range(self.n_steps -2, -1, -1):
            dt = self.time_grid[time_index + 1] - self.time_grid[time_index]
            if self.use_constant_discount:
                discount_factor = np.exp(-self.discount_curve * dt)
            else:
                discount_factor = np.exp(-self.discount_curve * dt)
                raise NotImplementedError("Non-constant discount curve not implemented")
            # perform regression for continuation value
            reg = self.__regression_types[self.default_type](asset_price[:, time_index], value[:, time_index + 1] * discount_factor, self.degree)
            continuation_value = self.__compute_cv(time_index, reg, asset_price)
            execise_value = np.zeros_like(asset_price[:, time_index])

            for j in range(self.n_paths):
                underlying_until_t = asset_price[j, 0:time_index] if time_index > 0 else asset_price[:, 0]
                execise_value[j] = self.payoff.eval(underlying_until_t)
            value[:, time_index] = (
                np.where(execise_value > continuation_value, execise_value, value[:, time_index + 1] * discount_factor))

        v_0 = value[:, 0] * np.exp(-self.underlying_instance.get_short_rate() * (self.time_grid[1]-self.time_grid[0]))
        value_0 = np.mean(v_0)
        self.v0_var = np.var(v_0)
        self.var_mc = self.v0_var / np.sqrt(self.n_paths)
        self.rmse = np.sqrt(np.mean(((v_0 - value_0) / self.n_paths) ** 2))
        self.value = value
        self.value_0 = value_0
        if return_type:
            return self.value_0, self.value, self.var_mc, self.rmse

    def __compute_cv(self, time_index, reg, asset_price):

        if self.default_type == "polynomial":
            continuation_value = np.polyval(reg, asset_price[:, time_index])
        else:
            continuation_value = np.zeros_like(asset_price[:, time_index])
            for j in range(self.n_paths):
                s_transformed = [ss.eval_legendre(deg, asset_price[j, time_index]) for deg in range(self.degree+1)]  # TODO: this needs a wrapper
                continuation_value[j] = np.dot(reg, s_transformed)
        return continuation_value
