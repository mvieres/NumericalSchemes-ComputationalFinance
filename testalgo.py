import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import longstaff_schwartz
from scipy.stats import norm

T = 1
N = 1000
n = 1000

degree = 5

r = 0.06
sigma = 0.2
s0 = 36
K = 36

M = Market(n=n, N=N, sigma=sigma, r=r, s0=s0, T=T)
d1 = (np.log(s0/K) + (r + 0.5*sigma**2)*T)
d2 = d1 - sigma*np.sqrt(T)
value_e = s0*norm.cdf(d1) - K*np.exp(-r)*norm.cdf(d2)

Value, var = longstaff_schwartz(Market=M, degree=degree, K=36, payoff="call", regression_type="polynomial")

print('Estimated value v_0 American: ', Value)
print('American Standard Variation: ', np.sqrt(var))
print('European Call value: ', value_e)
