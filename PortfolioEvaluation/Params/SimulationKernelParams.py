from typing import Dict

from PortfolioEvaluation.Params.HestonCIRParams import HestonCIRParams
from PortfolioEvaluation.Params.HestonCKLSParams import HestonCKLSParams
from PortfolioEvaluation.Params.StockOptionParams import StockOptionParams
from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.CIRParams import CIRParams
from PortfolioEvaluation.Params.CKLSParams import CKLSParams
from PortfolioEvaluation.Params.GeneralSimConfigParams import GeneralSimConfigParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams


class SimulationKernelParams:

    # Enforced structure self.job_requests = {"id": {"trade_params": self.trades, "simulation_params": {BlackScholesParams or else}}}
    def __init__(self):
        self.general_sim_params: GeneralSimConfigParams = GeneralSimConfigParams()
        # dict with key: id and value: dict with param classes for underlying, discount curve and fx
        self.sk_params: Dict[int, SimulationKernelParamsById] = {}

    def pull_from_input(self, portfolio: dict) -> None:
        """
        This class pulls the simulation kernel parameters from the input portfolio dictionary.
        @param portfolio:
        @return:
        """
        self.general_sim_params.from_dict(portfolio["simulation_config"])
        trades = portfolio["trades"]
        if not isinstance(trades, list):
            raise ValueError("Trades must be a list")
        for entry_dict in trades:
            if not len(list(entry_dict.keys())) == 1:
                raise ValueError("Trade entry must have exactly one key")
            trade_type = list(entry_dict.keys())[0]
            entry_dict_value = entry_dict[trade_type]
            trade_id = entry_dict_value["id"]
            self.sk_params[trade_id] = SimulationKernelParamsById()
            self.sk_params[trade_id].set_trade_params(entry_dict_value, trade_type)
        pass

    def set_general_sim_params(self, general_sim_params_dict: dict):
        self.general_sim_params.from_dict(general_sim_params_dict)

    def get_general_sim_params(self):
        return self.general_sim_params

    def set_sk_params(self, trade_id: int, underlying_params=None, interest_rate_params=None, fx_params=None):
        if trade_id not in self.sk_params:
            self.sk_params[trade_id] = SimulationKernelParamsById()
        self.sk_params[trade_id].set(underlying_params=underlying_params, discount_curve_params=interest_rate_params,
                                     fx_params=fx_params)

    def get(self, trade_id: int):
        return self.sk_params[trade_id]

    def get_all(self):
        return self.sk_params


class SimulationKernelParamsById:

    def __init__(self):
        self.trade_params = None
        self.underlying_params = None
        self.discount_curve_params = None
        self.fx_params = None

    def set(self, trade_params=None, underlying_params=None, discount_curve_params=None, fx_params=None):
        if trade_params is not None:
            assert isinstance(trade_params, StockOptionParams), "trade_params must be of type AbstractTradeParams"
            self.trade_params = trade_params

        if underlying_params is not None:
            assert isinstance(underlying_params,
                              BlackScholesParams or HestonCIRParams or TrolleSchwartzParams or CIRParams or CKLSParams), "underlying_params must be of type BlackScholesParams or HestonCIRParams or TrolleSchwartzParams"
            self.underlying_params = underlying_params

        if discount_curve_params is not None:
            assert (isinstance(discount_curve_params,
                              TrolleSchwartzParams) or isinstance(discount_curve_params, CIRParams)
                    or isinstance(discount_curve_params, CKLSParams)), "discount_params must be of type TrolleSchwartzParams or HestonCIRParams"
            self.discount_curve_params = discount_curve_params

        if fx_params is not None:
            assert isinstance(fx_params, HestonCIRParams), "fx_params must be of type HestonCIRParams or TrolleSchwartzParams"
            self.fx_params = fx_params

    def set_trade_params(self, trade_params_dict: dict, trade_type: str) -> None:
        if trade_type == "stock_option":
            self.trade_params = StockOptionParams()
        else:
            raise ValueError("Trade type not supported")
        self.trade_params.from_dict(trade_params_dict)

    def set_underlying_params(self, underlying_params: BlackScholesParams or HestonCIRParams or
                                                       HestonCKLSParams or TrolleSchwartzParams) -> None:
        self.underlying_params = underlying_params

    def set_discount_curve_params(self, discount_curve_params: TrolleSchwartzParams or CIRParams or CKLSParams) -> None:
        self.discount_curve_params = discount_curve_params

    def set_fx_params(self, fx_params: HestonCIRParams or HestonCKLSParams or TrolleSchwartzParams) -> None:
        self.fx_params = fx_params

    def get_trade_params(self):
        return self.trade_params

    def get_underlying_params(self):
        return self.underlying_params

    def get_discount_curve_params(self):
        return self.discount_curve_params

    def get_fx_params(self):
        return self.fx_params

    def get_all_sim(self):
        return self.underlying_params, self.discount_curve_params, self.fx_params


class SKParamsDictById:
    trade_params: StockOptionParams  # or other trade params class
    underlying_params: BlackScholesParams or HestonCIRParams or TrolleSchwartzParams
    interest_rate_params: TrolleSchwartzParams or HestonCIRParams
    fx_params: HestonCIRParams or TrolleSchwartzParams
