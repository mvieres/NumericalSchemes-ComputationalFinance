
import numpy as np


from OldFiles.market import Market
from OldFiles.algo import lsmc
from OldFiles.bs_theoretical_values import bs_call
import time

T = 1
N = 100000
n = 1000

degree = 4

r = 0.06
sigma = 0.2
s0 = 36
K = 33
payoff_structure = "call"
#reg = "legendre"
#reg = "polynomial"
reg = "polynomial"

start = time.time()
M = Market(n=n, paths=N, sigma=sigma, r=r, s0=s0, time_horizon=T)
Value, var, _ = lsmc(market=M, degree=degree, k=K, payoff=payoff_structure, regression_type=reg)
end = time.time()
theoretical_value = bs_call(s0=s0, strikeprice=K, timehorizon=T, r=r, sigma=sigma)

print('Estimated value at t=0 for American ' + str(payoff_structure) + ': ', Value)
print('American Standard Variation: ', np.sqrt(var))
print('European theoretical CALL value: ', theoretical_value)
print('Elapsed time: ' + str(end - start))
