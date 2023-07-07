import numpy as np
from scipy.stats import norm


def bs_call(s0, strikeprice, timehorizon, r, sigma):
    d1 = (np.log(s0 / strikeprice) + (r + sigma ** 2 / 2) * timehorizon) / (sigma * np.sqrt(timehorizon))
    d2 = d1 - sigma * np.sqrt(timehorizon)
    return s0 * norm(d1) - strikeprice * np.exp(-r * timehorizon) * norm(d2)
