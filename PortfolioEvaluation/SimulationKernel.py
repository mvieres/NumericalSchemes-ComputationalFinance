from logging import error
import numpy as np

from Market.BlackScholes import BlackScholes
from Market.Heston import Heston
from Market.TrolleSchwartz import TrolleSchwartz
from PortfolioEvaluation.Params.SimConfigParams import SimConfigParams
from Pricing.AmericanMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo
from Pricing.TheoreticalPrices import BlackScholesOptionPrices



class SimulationKernel:
    """
        SimulationKernel takes an object that has only primitive types (e.g. time information has to be double and not a sting)
        such that the actual modules like BlackScholes solver can be called.
    """
    def __init__(self, general_sim_params: SimConfigParams):
        self.general_sim_params = general_sim_params
        self.job_request = None
        self.models = {
            "BlackScholes": BlackScholes(0, 1, 1, 0, 0, 'euler', 'exposure'),
            "TrolleSchwartz": TrolleSchwartz(0, 1, 0, 0, 0, 0, 0 ,0, 0),
            "Heston": Heston(0, 1, 1, 0.1, 0, 1, 1, 1, 0.5, 'euler')
        }

    def set_job_request(self, job_request):
        self.job_request = job_request

    def get_job_result(self):
        return self.value

    def run(self):
        assert self.job_request is not None, "Job request is not set"
        model = self.job_request.get('model')
        sim_params = self.job_request["simulation_params"]
        trade_params = self.job_request["trade_params"]
        category = trade_params.get_category()
        model_instance = self.models.get(model)
        model_instance.pull_params(sim_params)  # This is very (!!!!) important otherwise the simulation runs with wrong parameters
        model_instance.generate_scenarios(self.general_sim_params.get_n_paths(), self.general_sim_params.get_discretization())

        if category == "stock_option":
            self.__process_stock_option(model_instance, model, sim_params, trade_params)
        if trade_params.get_quantity() is not None:
            self.value = trade_params.get_quantity() * self.value

    def __process_stock_option(self, model_instance, model, sim_params, trade_params):
        if model == "BlackScholes" and trade_params.get_exercise() == "european":
            tp_instance = BlackScholesOptionPrices(sim_params.t_start,
                                                   sim_params.t_end, sim_params.s0, sim_params.r, sim_params.sigma)
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
            lsm_instance = LongstaffSchwartzMonteCarlo(model_instance, payoff,
                                                       self.general_sim_params.n_paths,
                                                       self.general_sim_params.discretization)
            lsm_instance.compute_option_price()
            self.value = lsm_instance.value_0
        else:
            raise error("Process for stock option not succesfull")