import numpy as np
import matplotlib.pyplot as plt
from market import Market

n = 1000
N = 1
r = 0.0275
s0 = 10
T = 1
sigma = 0.2
kappa = 1
theta = 0.02
rho = 1
v0 = 1
xi = 0.9


M = Market(n=n, paths=N, r=r, s0=s0, time_horizon=T)

#S = M.black_scholes(sigma=sigma)
S, vol = M.heston_paths(kappa=kappa, theta=theta, v_0=v0, rho=rho, xi=xi, return_vol=True)
t = M.time_grid()
plt.plot(t, S, t, vol)

plt.legend('asset price', 'volatility')
plt.show()