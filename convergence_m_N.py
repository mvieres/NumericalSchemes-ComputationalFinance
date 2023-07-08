import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from market import Market
from algo import lsmc


T = 1
n = 100
sigma = 0.2
r = 0.06
s0 = 36
K = 40
reg = 'laguerre'
g = 'call'

N = np.arange(start=100, stop=10001, step=1000)  # Array
degree = np.arange(start=1, stop=101, step=10)  # Array

result = np.zeros(shape=(len(degree), len(N)))
result_var = np.zeros(shape=(len(degree), len(N)))
for i in range(len(degree)):
    for j in range(len(N)):
        M = Market(n=n, paths=N[j], sigma=sigma, r=r, s0=s0, time_horizon=T)
        result[i, j], result_var[i, j], _ = lsmc(market=M, degree=degree[i], k=K, payoff=g, regression_type=reg)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(degree, N)
surf = ax.plot_surface(X, Y, result_var, cmap=cm.coolwarm, linewidth=0)
plt.title('Variance in m and N')
plt.savefig('convergence_m_N.png')
plt.show()
