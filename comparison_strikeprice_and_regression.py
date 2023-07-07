import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import lsmc
from scipy.stats import norm

# Parameters
T = 1
N = 10000
n = 100
degree = 5
r = 0.06
sigma = 0.2
s0 = 36

# Initialize Market
M = Market(n=n, paths=N, sigma=sigma, r=r, s0=s0, time_horizon=T)
t = M.time_grid()
Stock = M.black_scholes()
K = np.linspace(1, 100, 100)
var = np.zeros_like(K)
reg = ['laguerre', 'legendre', 'polynomial']
results = np.zeros(shape=(len(reg)+1, len(K)))  # row-wise: different values in reg, col-wise: different values in K

for i in range(len(K)):
    print(K[i])
    d1 = (np.log(s0 / K[i]) + (r + 0.5*sigma**2) * T)
    d2 = d1 - sigma * np.sqrt(T)
    results[len(reg), i] = np.maximum(s0 * norm.cdf(d1) - K[i] * np.exp(-r) * norm.cdf(d2), 0)  # theoretical value
    for j in range(len(reg)):
        results[j, i], _, _ = lsmc(market=M, degree=degree, k=K[i], payoff="Call", regression_type=reg[j])


# Visualization
for j in range(len(results[:, 0])-1):
    plt.plot(K, results[j, :])
plt.plot(K, results[-1, :])
plt.axvline(s0, color='grey', linestyle='--')
plt.title('LSM with '+str(N)+' MC Runs and Grid-size '+str(n)+', s0 = '+str(s0))
plt.xlabel('Strike price K')
plt.ylabel('Estimated value at t=0')
plt.legend(['Laguerre', 'Legendre', 'Polynomial', 'Theoretical Value', 's0'])
plt.savefig('comparison_strike_price_regressiontypes.png')
plt.show()
