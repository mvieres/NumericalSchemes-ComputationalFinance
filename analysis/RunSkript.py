

from PortfolioEvaluation.RunPortfolioEvaluation import RunPortfolioEvaluation

runner_instance = RunPortfolioEvaluation(portfolio_name='C:/Users/pkv4e/Documents/GitHub/NumericalSchemes-ComputationalFinance/PortfolioEvaluation/portfolio.json')

runner_instance.run()
print(runner_instance.get_portfolio_value())

