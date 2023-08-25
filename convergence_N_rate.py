import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import lsmc


# Parameters
T = 1
K = 36
n = 100
degree = 4
r = 0.06
sigma = 0.2
s0 = 36

N = [10**i for i in range(1, 7)]  # Monte Carlo Runs
res_value = np.zeros(shape=(len(N),))  # Result Vector for estimated value
var = np.zeros(shape=(len(N,)))  # result vector for variance of estimated value
res_rmse = np.zeros(shape=(len(N,)))
z = 0
for i in N:
    print(i)
    M = Market(n=n, paths=i, r=r, s0=s0, time_horizon=T)
    s = M.black_scholes(sigma=sigma)
    res_value[z], var[z], res_rmse[z] = lsmc(assetprice=s, market=M, degree=degree, k=K, payoff="Call", regression_type="laguerre")
    z += 1



# Plot
plt.plot(np.log(N), np.log(var), 'x', color='black')
m, b = np.polyfit(np.log(N), np.log(var), 1)
plt.plot(np.log(N), m*np.log(N) + b, color='grey', linestyle='--')
plt.xticks(np.log(N), N)
plt.xlabel('N')
plt.ylabel('log(var)')
plt.legend(['lsmc variance', 'Regression coefficient: ' + str(m)])
plt.suptitle('Variance Reduction in N (log-log-plot)')
plt.title('Parameters: T=' + str(T) + ' K=' + str(K) + ' n=' + str(n) + ' m=' + str(degree) + ' r=' + str(r) + ' sigma='
          + str(sigma) + ' s0=' + str(s0))
plt.savefig('convergence_N_variance.png')
plt.show()
