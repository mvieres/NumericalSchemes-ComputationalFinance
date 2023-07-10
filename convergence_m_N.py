import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from market import Market
from algo import lsmc


T = 1
n = 50
sigma = 0.2
r = 0.06
s0 = 36
K = 40
reg = 'laguerre'
g = 'call'

N = np.arange(start=100, stop=10001, step=1000)  # Array
degree = np.arange(start=1, stop=1001, step=10)  # Array
#N = [10, 20, 50, 100, 100]
#degree = [1, 3, 5]
result = np.zeros(shape=(len(degree), len(N)))
result_var = np.zeros(shape=(len(degree), len(N)))
for i in range(len(degree)):
    for j in range(len(N)):
        M = Market(n=n, paths=N[j], sigma=sigma, r=r, s0=s0, time_horizon=T)
        result[i, j], result_var[i, j], _ = lsmc(market=M, degree=degree[i], k=K, payoff=g, regression_type=reg)

fig = plt.figure()
ax = plt.axes(projection='3d')
X, Y = np.meshgrid(np.log(N), degree)
ax.plot_surface(X, Y, np.log(result_var), cmap='viridis')
ax.set_xlabel('degree')
ax.set_ylabel('log(N)')
ax.set_zlabel('log(Variance)')
ax.set_title('Comparison m and N')
plt.show()
