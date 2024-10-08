@echo off
call .venv\Scripts\activate
python -m unittest discover -s ./Market/tests
python -m unittest discover -s ./NumericalSchemes/tests
python -m unittest discover -s ./Pricing/AmericanMonteCarlo/tests
python -m unittest discover -s ./Pricing/QuasiMonteCarlo/tests
python -m unittest discover -s ./Pricing/tests
python -m unittest discover -s ./PortfolioEvaluation/tests
python -m unittest discover -s ./MarketDataContainer/tests
