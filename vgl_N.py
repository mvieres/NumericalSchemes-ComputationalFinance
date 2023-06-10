import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import longstaff_schwartz, LSM
from scipy.stats import norm

T = 1
K = 36
n = 1000

degree = 4

r = 0.06
sigma = 0.2
s0 = 36


# Value = np.zeros(shape=(2,))

# Value = longstaff_schwartz(Market= M,degree = degree,K = 45)

N = np.array([100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 20000, 40000, 80000, 100000, 160000])
#N = np.array([100, 200, 400, 800])
res_value = np.zeros_like(N)

var = np.zeros_like(N)

z = 0
for l in N:
    print(l)
    M = Market(n=n, N=l, sigma=sigma, r=r, s0=s0, T=T)
    t = M.time_grid()
    BB = M.brownian_motion()
    Stock = M.black_scholes()
    res_value[z], var[z] = longstaff_schwartz(Market=M, degree=degree, K=K, payoff="Call",regression_type="polynomial")
    z = z + 1

d1 = (np.log(s0 / K) + (r + 0.5 * sigma ** 2) * T)
d2 = d1 - sigma * np.sqrt(T)
value_e = np.maximum(s0 * norm.cdf(d1) - K * np.exp(-r) * norm.cdf(d2), 0)
diff = np.abs(res_value - value_e)

plt.plot(N, diff)

plt.title('LSM with strike price ' + str(K) + ' and Gridsize ' + str(n) + ', s0 = ' + str(s0))
plt.xlabel('Number of Monte Carlo Runs')
plt.ylabel('Differnece')
plt.savefig('picture_vglN.png')
plt.show()