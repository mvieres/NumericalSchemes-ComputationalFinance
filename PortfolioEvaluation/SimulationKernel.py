from logging import error
import numpy as np

from Market.BlackScholes import BlackScholes
from Market.CIR import CIR
from Market.CKLS import CKLS
from Market.HestonCIR import HestonCIR
from Market.TrolleSchwartz import TrolleSchwartz
from PortfolioEvaluation.Params.SimulationKernelParams import SimulationKernelParamsById
from PortfolioEvaluation.Params.GeneralSimConfigParams import GeneralSimConfigParams
from Pricing.AmericanMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo
from Pricing.TheoreticalPrices import BlackScholesOptionPrices
from Utility.ModelEnum import ModelEnum as me


class SimulationKernel:
    """
        SimulationKernel takes an object that has only primitive types (e.g. time information has to be double and not a sting)
        such that the actual modules like BlackScholes solver can be called.
    """
    def __init__(self, general_sim_params: GeneralSimConfigParams):
        self.general_sim_params = general_sim_params
        self.job_request = None
        self.models = {
            me.BlackScholes.value: BlackScholes(0, 1, 1, 0, 0, 'euler', 'exposure'),
            me.HestonCir.value: HestonCIR(0, 1, 1, 0.1, 0, 1, 1, 1, 0.5, 'absolute_euler'),
            me.TrolleSchwartz.value: TrolleSchwartz(0, 1, 1, 0.1, 0, 1, 1, 1, 0.5, -0.3,'absolute_euler'),
            me.Cir.value: CIR(0, 1, 1, 0.1, 0.1, 0.1, 'absolute_euler'),
            me.CKLS.value: CKLS(0, 1, 1, 1, 1, 1, 1, 'absolute_euler')
        }
        self.underlying_sim = None
        self.discount_curve_sim = None
        self.fx_sim = None

    def set_job_request(self, job_request: SimulationKernelParamsById):
        # Check that the job request has at least underlying and trade params
        assert job_request.get_underlying_params() is not None, "Underlying params are not set"
        self.job_request = job_request

    def get_job_result(self):
        return self.value

    def run_new(self):
        """
            We simulate a single trade
            1) Identify the trade
            2) Identify the model
            3) Identify the simulation parameters
            4) roll out all market scenarios (not needed for BlackScholes)
            5) Go into pricing
        """
        if self.job_request is None:
            raise ValueError("Job request is not set")
        trade = self.job_request.get_trade_params().get_category()

        # Prepare simulation objects
        self.underlying_sim = self.models.get(self.job_request.get_underlying_params().get_model_name())
        self.underlying_sim.pull_params(self.job_request.get_underlying_params())
        if not self.general_sim_params.get_use_constant_interest_rate():
            self.discount_curve_sim = self.models.get(self.job_request.get_discount_curve_params().get_model_name())
            self.discount_curve_sim.pull_params(self.job_request.get_discount_curve_params())
        if self.job_request.get_trade_params().get_notional_currency() != self.general_sim_params.get_reference_yield_curve():
            self.fx_sim = self.models.get(self.job_request.get_fx_params().get_model_name())
            self.fx_sim.pull_params(self.job_request.get_fx_params())
        # Simulation of underlyings
        self.underlying_sim.generate_scenarios(self.general_sim_params.get_n_paths(), self.general_sim_params.get_discretization())
        if self.discount_curve_sim is not None:
            self.discount_curve_sim.generate_scenarios(self.general_sim_params.get_n_paths(), self.general_sim_params.get_discretization())
        if self.fx_sim is not None:
            self.fx_sim.generate_scenarios(self.general_sim_params.get_n_paths(), self.general_sim_params.get_discretization())

        # Pricing
        if trade == "stock_option":
            self.__process_stock_option_new()
        else:
            raise NotImplementedError("Trade type not implemented")
        pass

    def __process_stock_option_new(self) -> float:
        """
        This function processes a stock option trade given that the job request has only a stock option in it.
        @return:
        """
        trade_params = self.job_request.get_trade_params()
        if self.general_sim_params.get_use_constant_interest_rate():
            r = self.job_request.get_discount_curve_params().get_r()  # Here we should get r0 from some curve, i.e. sim_underlying
        else:
            r = self.discount_curve_sim.get_short_rate()  # Should be a vector (length of n_steps) TODO: Wrong
        if trade_params.get_exercise() == "european":
            if self.job_request.get_underlying_params().get_model_name() == me.BlackScholes:
                # This is the case for exact pricing
                # TODO: Mapping for european black scholes and non constant interest rate; ???
                tp_instance = BlackScholesOptionPrices(self.job_request.get_underlying_params().get_t_start(),
                                                       self.job_request.get_underlying_params().get_t_end(),
                                                       self.job_request.get_underlying_params().get_starting_point(),
                                                        r,
                                                       self.job_request.get_underlying_params().get_sigma())
                if trade_params.get_type() == "put":
                    value = tp_instance.put_option_theoretical_price(trade_params.get_strike())
                elif trade_params.get_type() == "call":
                    value = tp_instance.call_option_theoretical_price(trade_params.get_strike())
                else:
                    raise ValueError("Option type not implemented")
            else:
                raise NotImplementedError("General Monte Carlo not implemented yet")
        elif trade_params.get_exercise() == "american":
            raise NotImplementedError("American option pricing not implemented yet")
        else:
            raise ValueError("Typo in exercise type")
        return value

    def run(self):
        assert self.job_request is not None, "Job request is not set"
        model = self.job_request.get('model')
        sim_params_model = self.job_request["simulation_params"]["underlying"]
        sim_params_interest = self.job_request["simulation_params"]["interest_rate"]
        trade_params = self.job_request["trade_params"]
        category = trade_params.get_category()
        model_instance = self.models.get(model)
        model_instance.pull_params(sim_params_model)  # This is very (!!!!) important otherwise the simulation runs with wrong parameters
        model_instance.generate_scenarios(self.general_sim_params.get_n_paths(), self.general_sim_params.get_discretization())
        # For non-constant interest rates, generate scenarios for the interest rate
        if self.general_sim_params.get_use_constant_interest_rate():
            interest_instance = 0.01  # Just for now; TODO: constant interest rate pull from mkd or
        else:
            interest_instance = self.models.get("interest_rate")
            interest_instance.pull_params(sim_params_interest)  # Here we need to get the right params for correct interest rate curve
        if category == "stock_option":
            self.__process_stock_option(model_instance, model, interest_instance, sim_params_model, trade_params)
        if trade_params.get_quantity() is not None:
            self.value = trade_params.get_quantity() * self.value

    def __process_stock_option(self, model_instance, model, interest_instance, sim_params, trade_params):
        # TODO Adapt this to the new structure
        if model == "BlackScholes" and trade_params.get_exercise() == "european":
            tp_instance = BlackScholesOptionPrices(sim_params.get_t_start(),
                                                   sim_params.get_t_end(), sim_params.get_starting_point(),
                                                   sim_params.get_r(), sim_params.get_sigma())
            if trade_params.get_type() == "put":
                self.value = tp_instance.put_option_theoretical_price(trade_params.get_strike())
            elif trade_params.get_type() == "call":
                self.value = tp_instance.call_option_theoretical_price(trade_params.get_strike())
            else:
                raise ValueError("Option type not implemented")

        elif trade_params.get_exercise() == "american":
            if trade_params.get_type() == "put":
                payoff = lambda x: np.maximum(trade_params.get_strike() - x, 0)
            elif trade_params.get_type() == "call":
                payoff = lambda x: np.maximum(x - trade_params.get_strike(), 0)
            else:
                raise ValueError("Option type not implemented / Payoff error")
            lsm_instance = LongstaffSchwartzMonteCarlo(model_instance, payoff, self.general_sim_params.n_paths,
                                                       self.general_sim_params.discretization)
            lsm_instance.compute_option_price()
            self.value = lsm_instance.value_0
        else:
            raise error("Process for stock option not succesfull")