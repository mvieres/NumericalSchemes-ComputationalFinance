

from PortfolioEvaluation.RunPortfolioEvaluation import RunPortfolioEvaluation

runner_instance = RunPortfolioEvaluation(portfolio_name='C:/Users/MV_2/Documents/GitHub/lMS-monte-carlo/PortfolioEvaluation/portfolio.json')

runner_instance.run()
print(runner_instance.get_portfolio_value())

