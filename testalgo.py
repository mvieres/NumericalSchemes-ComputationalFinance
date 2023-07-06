import numpy as np


from market import Market
from algo import lsmc
from scipy.stats import norm

T = 1
N = 100000
n = 100

degree = 10

r = 0.06
sigma = 0.2
s0 = 36
K = 33
payoff_structure = "call"
reg = "legendre"
#reg = "polynomial"


M = Market(n=n, paths=N, sigma=sigma, r=r, s0=s0, time_horizon=T)
d1 = (np.log(s0/K) + (r + 0.5*sigma**2)*T)
d2 = d1 - sigma*np.sqrt(T)
value_e = s0*norm.cdf(d1) - K*np.exp(-r)*norm.cdf(d2)  # Theoretical Values

Value, var, _ = lsmc(market=M, degree=degree, k=K, payoff=payoff_structure, regression_type=reg)

print('Estimated value at t=0 for American ' + str(payoff_structure) + ': ', Value)
print('American Standard Variation: ', np.sqrt(var))
print('European theoretical CALL value: ', value_e)
