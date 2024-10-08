import unittest

from PortfolioEvaluation.Params.BlackScholesParams import BlackScholesParams
from PortfolioEvaluation.Params.HestonParams import HestonParams
from PortfolioEvaluation.Params.StockOptionParams import StockOptionParams
from PortfolioEvaluation.Params.TrolleSchwartzParams import TrolleSchwartzParams
from PortfolioEvaluation.RunPortfolioEvaluation import RunPortfolioEvaluation


class RunPortfolioEvaluationTest(unittest.TestCase):

    def test_run_functionality(self):
        runner_instance = RunPortfolioEvaluation(portfolio_name='C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/portfolio.json')
        try:
            runner_instance.run()
        except Exception as e:
            self.fail(e)


    def test_process_default_models(self):
        runner_instance = RunPortfolioEvaluation(portfolio_name='C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/portfolio.json')
        default_dict = {
            "stock_option": "BlackScholes",
            "interest_rate": "TrolleSchwartz",
            "foreign_exchange": "Heston"
        }
        supposed_dict = {
            "stock_option": BlackScholesParams(),
            "interest_rate": TrolleSchwartzParams(),
            "foreign_exchange": HestonParams(),
        }
        result = runner_instance.process_default_models(default_dict)
        for key in result.keys():
            self.assertTrue(isinstance(result[key], supposed_dict[key].__class__))

    def test_get_params(self):
        runner_instance = RunPortfolioEvaluation(portfolio_name='C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/portfolio.json')
        input_list = [{'stock_option': {'company': 'APPL', 'exercise': 'european', 'id': 1111, 'maturity': '2024-12-10',
                           'notional_currency': 'USD', 'quantity': 1, 'strike': 100, 'type': 'call'}}, {
             'stock_option': {'company': 'ADS', 'exercise': 'european', 'id': 1112, 'maturity': '2024-12-10',
                              'notional_currency': 'USD', 'quantity': 1, 'strike': 100, 'type': 'put'}}]
        runner_instance.trades = input_list
        runner_instance.read_portfolio()
        runner_instance.get_params()
        for trade in runner_instance.trades:
            self.assertTrue(isinstance(trade['stock_option'], StockOptionParams))


if __name__ == '__main__':
    unittest.main()
