from typing import TypedDict, Dict

from PortfolioEvaluation.Params.AbstractTradeParams import AbstractTradeParams
from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.SimConfigParams import SimConfigParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams


class SimulationKernelParams:
    # Enforced structure self.job_requests = {"id": {"trade_params": self.trades, "simulation_params": {BlackScholesParams or else}}}
    def __init__(self):
        self.__general_sim_params: SimConfigParams = SimConfigParams()
        # dict with key: id and value: dict with param classes for underlying, interest_rate, fx
        self.__sk_params: Dict[int, SimulationKernelParamsById] = {}

    def set_general_sim_params(self, general_sim_params_dict: dict):
        self.__general_sim_params.from_dict(general_sim_params_dict)

    def get_general_sim_params(self):
        return self.__general_sim_params

    def set_sk_params(self, trade_id: int, underlying_params=None, interest_rate_params=None, fx_params=None):
        if trade_id not in self.__sk_params:
            self.__sk_params[trade_id] = SimulationKernelParamsById()
        self.__sk_params[trade_id].set(underlying_params=underlying_params, interest_rate_params=interest_rate_params, fx_params=fx_params)

    def get(self, trade_id: int):
        return self.__sk_params[trade_id]


class SimulationKernelParamsById:
    def __init__(self):
        self.__sk_params_per_trade_id: TypedDict[SKParamsDictById] = {}

    def set(self, trade_params=None, underlying_params=None, interest_rate_params=None, fx_params=None):
        if trade_params is not None:
            assert isinstance(trade_params, AbstractTradeParams), "trade_params must be of type AbstractTradeParams"
            self.__sk_params_per_trade_id["trade_params"] = trade_params

        if underlying_params is not None:
            assert isinstance(underlying_params, BlackScholesParams or HestonCIRParams or TrolleSchwartzParams), "underlying_params must be of type BlackScholesParams or HestonCIRParams or TrolleSchwartzParams"
            self.__sk_params_per_trade_id["underlying_params"] = underlying_params

        if interest_rate_params is not None:
            assert isinstance(interest_rate_params, TrolleSchwartzParams or HestonCIRParams), "interest_rate_params must be of type TrolleSchwartzParams or HestonCIRParams"
            self.__sk_params_per_trade_id["interest_rate_params"] = interest_rate_params

        if fx_params is not None:
            assert isinstance(fx_params, HestonCIRParams or TrolleSchwartzParams), "fx_params must be of type HestonCIRParams or TrolleSchwartzParams"
            self.__sk_params_per_trade_id["fx_params"] = fx_params

    def get_params(self):
        return self.__sk_params_per_trade_id

    def get_trade_params(self):
        return self.__sk_params_per_trade_id["trade_params"]

    def get_underlying_params(self):
        return self.__sk_params_per_trade_id["underlying_params"]

    def get_interest_rate_params(self):
        return self.__sk_params_per_trade_id["interest_rate_params"]

    def get_fx_params(self):
        return self.__sk_params_per_trade_id["fx_params"]


class SKParamsDictById:
    trade_params: AbstractTradeParams
    underlying_params: BlackScholesParams or HestonCIRParams or TrolleSchwartzParams
    interest_rate_params: TrolleSchwartzParams or HestonCIRParams
    fx_params: HestonCIRParams or TrolleSchwartzParams
