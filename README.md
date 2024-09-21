# Numerical Schemes and Monte Carlo Methods for Stochastic Processes
Author: **Maximilian Vieres** [mvieres@outlook.com]\
Version: **0.1.0**

**Note: This module is a work in progress.**

This repository provides modules for various applications in the field of stochastic processes, with a primary focus on numerical schemes and Monte Carlo methods for stochastic differential equations (SDEs). While these techniques are commonly applied in mathematical finance, they also find uses in other fields, such as geological research through Monte Carlo methods.

The repository aims to evaluate a portfolio, as outlined in portfolio.json. To achieve this, the repository is divided into the following submodules:

- NumericalSchemes: Implements common stochastic objects and numerical schemes for SDEs, such as Brownian motion and the Euler-Maruyama scheme.
- MonteCarlo: Implements general Monte Carlo methods for SDEs.
- Market: Contains market models used to evaluate the portfolio, such as the Black-Scholes or Heston models.
- Pricing: Provides techniques for evaluating various types of financial trades.

The most important design principle is to keep NumericalSchemes and MonteCarlo as general as possible, allowing their use in broader applications. Meanwhile, Market and Pricing are more specific and rely heavily on the first two modules.

## Numerical Schemes
Numerical methods for stochastic processes are crucial, with the Euler-Maruyama scheme being the most widely used. Other schemes, like the Milstein and Runge-Kutta methods, offer potentially higher convergence rates.

However, when dealing with random processes, particularly Brownian motion (which has low regularity), the speed of convergence for numerical schemes is limited by the discretization of the Brownian motion itself. As a result, the Euler-Maruyama scheme is often preferred, though variations derived from Euler's method are useful in specialized cases.

This module offers a collection of the most relevant schemes and approaches to handle a wide range of problems. Further details on these schemes and their theoretical foundations will be included in the methodological documentation (still in progress).

## Monte Carlo
The MonteCarlo module implements the Multi-Level Monte Carlo (MLMC) method. Since the basic Monte Carlo estimator is simply the standard expectation estimator, no additional module is needed for this standard case.
There are various techniques to reduce variance in Monte Carlo estimators, such as MLMC and importance sampling. These advanced methods are still under development.

## Market
When modeling "the market," several considerations must be addressed:

1) What constitutes the market?
2) What are its properties?
3) How is information stored and processed?
4) How is market data stored?
5) How do we distinguish between real market data and simulated data?
6) Currently, the most abstract version of a market is implemented in the AbstractMarket class, found in AbstractMarket.py. This class consists of a time grid, a starting price, and a constant risk-free rate. It does not specify any asset prices, as it serves as a foundation for market models rather than a complete implementation.

The "Abstract" prefix indicates that this class focuses on the fundamental aspects of a market and follows naming conventions similar to those in Java. Every specific market model should inherit from this class and implement its methods, most notably the generate_scenarios method.

## Pricing
Pricing financial products is theoretically straightforward. For certain models, closed-form solutions for prices exist and should be used when available. A prominent example is the pricing of put and call options under the Black-Scholes model.

In cases where no closed-form solutions exist, Monte Carlo methods are used to evaluate the price, as these methods are model-independent. However, when a specific model is used, the Monte Carlo estimators can be optimized accordingly. For more information, refer to the methodological documentation.

### European Options
Under the Black-Scholes model, there are closed-form solutions for pricing European put and call options.

### American Options
Currently, the only implemented pricing technique for American options is the Longstaff-Schwartz algorithm, which is available in the LongstaffSchwartzMonteCarlo class within LongstaffSchwartzMonteCarlo.py. The class can be initialized with the following parameters:

### Quasi-Monte Carlo
This section introduces Quasi-Monte Carlo methods, which are used to evaluate swaps. These methods are not included under the Monte Carlo section because Quasi-Monte Carlo is technically not a Monte Carlo method.

# Portfolio Evaluation
The repository also contains a module to evaluate a portfolio of trades. As of now, the basic framework and value for European call / put options is implemented.
An example for such a portfolio is provided in portfolio.json.