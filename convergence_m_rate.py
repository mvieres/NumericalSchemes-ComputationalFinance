import numpy as np
import matplotlib.pyplot as plt
from bs_theoretical_values import bs_call
from market import Market
from algo import lsmc


# Parameters
T = 1
K = 40
n = 100
degree = 4
r = 0.06
sigma = 0.2
s0 = 36

N = 10000
m = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50])  # degrees
res_value = np.zeros(shape=(len(m),))  # Result Vector for estimated value
var = np.zeros(shape=(len(m,)))  # result vector for variance of estimated value
res_rmse = np.zeros(shape=(len(m,)))
z = 0
for i in m:
    print(i)
    M = Market(n=n, paths=N, sigma=sigma, r=r, s0=s0, time_horizon=T)
    res_value[z], var[z], res_rmse[z] = lsmc(market=M, degree=i, k=K, payoff="Call", regression_type="laguerre")
    z += 1

theoretical_value = bs_call(s0=s0, strikeprice=K, timehorizon=T, r=r, sigma=sigma)

res_diff = np.abs(res_value - theoretical_value)
# Plot
plt.plot(m, res_diff, 'x', color='black')
inc, b = np.polyfit(m, var, 1)
plt.plot(m, inc*var + b, color='grey', linestyle='--')
plt.xlabel('degree')
plt.ylabel('Variance')
plt.legend(['Difference', 'Regression coefficient: ' + str(inc)])

plt.title('Parameters: T=' + str(T) + ' K=' + str(K) + ' n=' + str(n) + ' paths=' + str(N) + ' r=' + str(r) + ' sigma='
          + str(sigma) + ' s0=' + str(s0))
plt.savefig('convergence_m.png')
plt.show()
