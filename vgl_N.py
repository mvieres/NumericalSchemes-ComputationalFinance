import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import longstaff_schwartz
from scipy.stats import norm
from sklearn.linear_model import LinearRegression


# Parameters
T = 1
K = 36
n = 100
degree = 4
r = 0.06
sigma = 0.2
s0 = 36

N = np.arange(start=100, stop=10001, step=100)  # Monte Carlo Runs
res_value = np.zeros(shape=(len(N),))  # Result Vector for estimated value
var = np.zeros_like(N)  # result vector for variance of estimated value

z = 0
for i in N:
    print(i)
    M = Market(n=n, N=i, sigma=sigma, r=r, s0=s0, T=T)
    a, b = longstaff_schwartz(Market=M, degree=degree, K=K, payoff="Call", regression_type="polynomial")
    print(a)
    res_value[z] = a
    var[z] = b
    z = z + 1

d1 = (np.log(s0 / K) + (r + 0.5 * sigma ** 2) * T)
d2 = d1 - sigma * np.sqrt(T)
value_e = np.maximum(s0 * norm.cdf(d1) - K * np.exp(-r) * norm.cdf(d2), 0)
diff = np.abs(res_value - value_e)

# Regression
N_res = N.reshape(-1, 1)
diff_res = diff.reshape(-1, 1)
lin_reg = LinearRegression()
lin_reg.fit(N_res, diff_res)
diff_pred = lin_reg.predict(N_res)

print(res_value)
print("Linear Regression coefficient:" + str(lin_reg.coef_))
plt.plot(N, diff)
plt.plot(N, diff_pred, color='red')
plt.title('LSM with strike price ' + str(K) + ' and Grid-size ' + str(n) + ', s0 = ' + str(s0))
plt.xlabel('Number of Monte Carlo Runs')
plt.ylabel('Difference')
plt.savefig('picture_vglN.png')
plt.show()
