import unittest
import json

from PortfolioEvaluation.Params.SimulationKernelParams import SimulationKernelParams


class SimulationKernelParamsTest(unittest.TestCase):

    def test_functionality(self):

        try:
            with open('C:/Users/MV_2/Documents/GitHub/lMS-monte-carlo/PortfolioEvaluation/portfolio.json', 'r') as file:
                data = json.load(file)
            sk_params = SimulationKernelParams()
            sk_params.pull_from_input(data)
            print(sk_params.get_all())
        except Exception as e:
            print(e)
            self.fail("Functionality not given")
