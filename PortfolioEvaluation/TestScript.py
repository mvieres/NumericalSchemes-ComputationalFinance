import json

from PortfolioEvaluation.PortfolioParams import PortfolioParams

file_path = 'Portfolio.json'

with open(file_path, 'r') as file:
    data = json.load(file)

portfolio_params = PortfolioParams()

portfolio_params.from_dict(data)

stop = 0