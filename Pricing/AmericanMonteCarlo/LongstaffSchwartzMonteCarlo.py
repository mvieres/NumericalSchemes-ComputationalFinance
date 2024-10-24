import numpy as np
import scipy.special as ss

from Market.BlackScholes import BlackScholes
from Market.HestonCIR import HestonCIR
from Market.HestonCKLS import HestonCKLS


class LongstaffSchwartzMonteCarlo:
    """
    AMC for american Put and Call Options .
    """

    def __init__(self, underlying_instance: BlackScholes or HestonCIR or HestonCKLS,
                 payoff: callable, payoff_type: str, n_paths: int, n_steps: int):
        self.underlying_instance = underlying_instance
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.__check_for_market_scenarios()
        self.payoff = payoff
        self.payoff_type = payoff_type
        assert payoff_type == "path_independent" or payoff_type == "path_dependent", "Typo??"
        self.default_type = "polynomial"
        self.time_grid = underlying_instance.time_grid_instance.get_time_grid(self.n_steps)
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
        self.var_mc = None
        self.value = None
        self.value_0 = None
        self.rmse = None
        self.v0_var = None

    def payoff_wrapper(self, x: np.ndarray or float):
        """
        Input is a numpy array of asset price path until time point t.
        The input is either a whole path or a single value. Note: When evaluating at t=0,
        the input for pathdependent is also a single value.
        :param x: np.array or float
        """
        if isinstance(x, float) or isinstance(x, int):
            return self.payoff(x)
        if self.payoff_type == "path_independent":
            return self.payoff(x[-1])
        if self.payoff_type == "path_dependent":
            return self.payoff(x)

    def set_degree(self, degree: int) -> None:
        self.degree = degree

    def set_payoff(self, payoff: callable) -> None:
        self.payoff = payoff

    def set_regression_type(self, regressiontype: str):
        self.default_type = regressiontype

    def generate_samples(self):
        self.underlying_instance.compute_solution_path(self.n_steps)

    def __check_for_market_scenarios(self):
        if len(self.underlying_instance.scenarios.keys()) == 0:
            self.underlying_instance.generate_scenarios(n_paths=self.n_paths, n_steps=self.n_steps)
        else:
            assert len(self.underlying_instance.scenarios) == self.n_paths, "Number of paths must be equal to number of scenarios"

    def compute_option_price(self, return_type=False) -> np.array:
        asset_price = np.zeros(shape=(self.n_paths, self.n_steps))
        for key in self.underlying_instance.scenarios.keys():
            if self.underlying_instance.dimension == 2:
                asset_price[key] = self.underlying_instance.scenarios[key][:, 0]
            else:
                asset_price[key] = self.underlying_instance.scenarios[key]
        value = np.zeros_like(asset_price)
        for path in range(self.n_paths):
            value[path, -1] = self.payoff_wrapper(asset_price[path, :])
        #value[:, -1] = self.payoff(asset_price[:, -1])
        for time_index in range(self.n_steps -2, -1, -1):
            dt = self.time_grid[time_index + 1] - self.time_grid[time_index]
            discount = np.exp(-self.underlying_instance.get_short_rate()*dt)
            # perform regression for continuation value
            reg = self.__regression_types[self.default_type](asset_price[:, time_index], value[:, time_index + 1] * discount, self.degree)
            continuation_value = self.__compute_cv(time_index, reg, asset_price)
            execise_value = np.zeros_like(asset_price[:, time_index])


            for j in range(self.n_paths):
                underlying_until_t = asset_price[j, 0:time_index] if time_index > 0 else asset_price[:, 0]
                execise_value[j] = self.payoff_wrapper(underlying_until_t)
            value[:, time_index] = (
                np.where(execise_value > continuation_value, execise_value, value[:, time_index + 1] * discount))

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
