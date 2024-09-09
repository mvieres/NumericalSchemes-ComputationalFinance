import numpy as np
import scipy.special as ss


def call(x, k):
    return np.maximum(0, x - k)


def put(x, k):
    return np.maximum(0, k - x)


def arithmetic_asian_call(x, k, n):
    return np.max((1 / n) * np.sum(x - k), 0)


def lsmc(assetprice, market, degree, k, payoff, regression_type):
    """
    Performs the least-squares-monte-carlo algorithm using all paths

    Note: Asset Price must be supplied outside the function
    @param assetprice: Prices
    @param market: Market env, just to get the parameters. Could be extracted from assetprice.
    @param degree: maximum of degrees for regression
    @param k: strike price
    @param payoff: payoff structor of option
    @param regression_type: regression to be used (polynomial / legendre)
    @return: estimated value value_0, variance, RootSquaredMeanError
    """

    # Extracting t, s from Market environment
    t = market.time_grid()
    r = market.r
    paths = market.N
    n = market.n
    delta_t = t[1] - t[0]  # delta time
    num_steps = t.shape[0]  # Number of time steps (col-dimensions)
    num_mc = assetprice.shape[0]  # Number of monte carlo runs (row-dimensions)
    discount = np.exp(-r * delta_t)  # Constant discount factor for equidistant grid
    value = np.zeros_like(assetprice)  # Pre-allocation for value

    # Processing input string of option payoff
    if payoff.lower() == "call":
        def g(a):
            return call(a, k)
    elif payoff.lower() == "put":
        def g(a):
            return put(a, k)
    elif payoff.lower() == "arithmetic_asian_call":
        def g(a):
            return arithmetic_asian_call(a, k=k, n=n)
    else:
        print("No valid Option chosen")
        return

    # Processing Regression type and setting flag to use in for-loop
    print('Chosen Basis Polynomials: ' + regression_type)
    if regression_type.lower() == "legendre":
        flag = 1
    elif regression_type.lower() == "laguerre":
        flag = 2
    elif regression_type.lower() == "polynomial":
        flag = 3
    else:
        print('No valid regression type chosen')
        return

    # Beginning of computation
    value[:, -1] = g(assetprice[:, -1])  # Compute Value for Last Time point
    # Iteration backwards in Time
    for t in range(num_steps - 2, -1, -1):
        # Regression
        if flag == 1:
            reg = np.polynomial.legendre.legfit(assetprice[:, t], value[:, t + 1] * discount, deg=degree)
            continuation_value = np.zeros_like(value[:, -1])
            for j in range(num_mc):
                s_transformed_j = [ss.eval_legendre(deg, assetprice[j, t]) for deg in range(degree+1)]
                continuation_value[j] = np.dot(reg, s_transformed_j)
        elif flag == 2:
            reg = np.polynomial.laguerre.lagfit(assetprice[:, t], value[:, t + 1] * discount, deg=degree)
            continuation_value = np.zeros_like(value[:, -1])
            for j in range(num_mc):
                s_transformed_j = ss.eval_laguerre(range(degree+1), assetprice[j, t])
                continuation_value[j] = np.dot(reg, s_transformed_j)
        else:
            reg = np.polyfit(assetprice[:, t], value[:, t + 1] * discount, deg=degree)
            continuation_value = np.polyval(reg, assetprice[:, t])

        # Compute exercise value
        ex_val = np.zeros_like(assetprice[:, t])
        for j in range(num_mc):  # for loop structure because g takes only single values
            ex_val[j] = g(assetprice[j, t])

        # Update Value Array
        value[:, t] = np.where(ex_val > continuation_value, ex_val, value[:, t + 1] * discount)

    # Standard Monte Carlo
    v_0 = value[:, 0] * discount
    value_0 = np.mean(v_0)
    v0_var = np.var(v_0)
    var_mc = v0_var / np.sqrt(paths)
    rmse = np.sqrt(np.mean(((v_0 - value_0) / paths)**2))

    return value_0, var_mc, rmse
