import numpy as np
from numpy.polynomial import legendre



def Call(x, K):
    return np.maximum(0, x - K)


def Put(x, K):
    return np.maximum(0, K - x)


def Arithmetic_Asian_Call(x, K, n):
    return np.max((1 / n) * np.sum(x - K), 0)


def longstaff_schwartz(Market, degree, K, payoff, regression_type):
    """Performs the Least squares Monte Carlo Estimation for American Put(!!) Options. Uses Black Scholes Model as underlying Market Model

    Args:
        Market (Array): on axis 0: Sample paths, on axis 1 values at each time point for a given sample path
        degree (int): Maximum polynomial degree to be considered for regression
        K (float): strike price
        payoff (string): Payoff function of Option
    Returns:
        float: Estimated value of american Option
    """

    # Extracting t, S from Market environment
    t = Market.time_grid()
    S = Market.black_scholes()
    r = Market.r
    N = Market.N
    n = Market.n

    # Processing input string of option payoff
    if payoff.lower() == "call":
        def g(a): return Call(a, K)
    elif payoff.lower() == "put":
        def g(a): return Put(a, K)
    elif payoff.lower() == "arithmetic_asian_call":
        def g(a): return Arithmetic_Asian_Call(a, K=K, n=n)
    else:
        print("No valid Option chosen")
        return

    # Processing Regression type and setting flag to use in for-loop
    print('Chosen Basis Polynomials: ' + regression_type)
    if regression_type.lower() == "legendre":
        flag = True
    else:
        flag = False

    delta_t = t[1] - t[0]  # delta time
    num_steps = t.shape[0]  # Number of time steps (col-dimensions)
    num_mc = S.shape[0]  # Number of monte carlo runs (row-dimensions)

    discount = np.exp(-r * delta_t)  # Constant discount factor for equidistant grid
    value = np.zeros_like(S)  # Pre-allocation for value

    # Compute Value for Last Time point, i.e g()
    for j in range(num_mc):
        value[j, -1] = g(S[j, -1])

    # Iteration backwards in Time
    for t in range(num_steps - 2, -1, -1):

        if flag:
            # TODO: Fix Legendre
            reg = legendre.legfit(S[:, t], value[:, t + 1] * discount, degree)[0]
        else:
            reg = np.polyfit(S[:, t], value[:, t + 1] * discount, deg=degree)
        # TODO: ADD estimation of contin_val via neural network
        contin_val = np.polyval(reg, S[:, t])

        # Exercise value
        ex_val = np.zeros_like(S[:, t])
        for j in range(num_mc):
            ex_val[j] = g(S[j, t])

        for j in range(num_mc):
            if ex_val[j] >= contin_val[j]:
                value[j, t] = g(S[j, t])
            else:
                value[j, t] = value[j, t + 1]

        # Standard Monte Carlo 
        v_0 = value[:, 0]  #* discount
        value_0 = np.mean(v_0)
        v0_var = np.var(v_0)
        var_mc = v0_var / N

    return value_0, var_mc
