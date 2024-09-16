# Numerical Schemes and Monte-Carlo for stochastic processes

**Author**: Maximilian Vieres [mvieres@outlook.com]\
**Version**: 0.1.0

**This module is work-in-progress**


This repository contains moduls for various purposes in the field of stochastic processes. 
The main focus is on numerical schemes and Monte-Carlo methods for stochastic differential equations (SDEs).
Most common application for those theories are in the field of mathematical finance, but other fields, such as geological research, borrow from Mont-Carlo-techniques.
Hence, the repository sets its goal on evaluating a portfolio of the structure as shown in portfolio.json. In order to do this, the repo is divided into small submodules:
- **NumericalSchemes**: Contains the implementation of the most common stochastic objects and numerical schemes for SDEs, e.g. the Brownian motion and Euler-Maruyama scheme.
- **MonteCarlo**: Contains the implementation of the Monte-Carlo-method for SDEs in a general setting.
- **Market**: Contains the implementation of a market model, which is used to evaluate the portfolio, e.g. the Black-Scholes model or Heston.
- **Pricing**: Contains various techniques to evaluate different types of trades.

The most important design principe is to keep the modules **NumericalSchemes** and **MonteCarlo** as general as possible, such that they can be used in other applications.
The modules **Market** and **Pricing** are more specific and highly depend the first two modules.

## Numerical Schemes
In the field of numerics for stochastic processes, there are many schemes. The most commen one is the Euler-Maruyama scheme. Notable mentions with potential higher convergence rates are milstein and Runge-Kutta schemes.
However, when it comes to random processes, the most important object is the Brownian motion, which has low regularity. Hence, convergence speed for numerical schemes is limited by the discretization of the Brownian motion.
As a direct consequence, the Euler-Maruyama scheme is commonly used. Nevertheless, there are more schemes that are derived from Euler and are used in specialized cases.
This module tries to offer a collection of the most useful ideas and schemes to tackle as many problems as possible.
Details on the schemes and their theoretical background can be find in the methodological documentation (which is not yet completed).


## Monte-Carlo
The **Monte-Carlo** module contains the implementation of the Multi-Level-Monte-Carlo idea.
As the standard Monte-Carlo estimator is given by the typical expectation estimator, we do not need to implement a module for this idea.
However, there are various ways to reduce variance in Monte-Carlo estimators, e.g. MLMC and importance sampling. (Work in progress)

## Market
When implementing "the market", we have to consider the following:
- What does the market consist of?
- What are the markets properties?
- How to store / process the information?
- How to store market data?
- How to separate the market data from simulated market data?

Currently, the most abstract idea of "a market" is implemented in the class `AbstractMarket` in the file `AbstractMarket.py`. It simply consists of a time grid, starting price and a constant risk-free rate. 
As this class does not specify any model, it has no asset prices. The prefix "Abstract" suggest that this class only elaborates on the most basic ideas of what the market should look like and borrows its naming-convention from java-implements.
Hence, every market model should inherit from this class and "implement" it's methods; most notably the `generate_scenarios` method.



## Pricing
The general setup for pricing financial products is in theory straight forward. Depending on the underlying model, there might be a closed formula for the price.
If this is the case, those closed solutions should be used. The most prominent example are Put- and Call-Options under the Black-Scholes model.
If there are no closed formulas, Monte-Carlo methods are used to evaluate the price. This Monte-Carlo approach is per se model independent.
However, when fixing an underlying model, the Monte-Carlo estimators can be optimized and might look differently. The interested reader is referred to the methodological documentation for more details.

### European Option
Under the Black-Scholes model, Put- and Call-Options have a closed formula.

### Amercian Option
Currently the only pricing technique implemented is the Longstaff-Schwartz algorithm for American options. The algorithm is implemented in the class `LongstaffSchwartzMonteCarlo` in the file `LongstaffSchwartzMonteCarlo.py`. The class is initialized with the following parameters:


### Quasi-Monte-Carlo
This contains a section to Quasi-Monte-Carlo methods, which are used to evaluate swaps. This is not put under the section of **Monte-Carlo** as Qusi-Monte-Carlo is technically not a Monte-Carlo method. 

