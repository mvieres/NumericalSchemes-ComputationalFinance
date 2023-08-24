import numpy as np
import matplotlib.pyplot as plt
from market import Market

n = 1000
N = 2
r = 0.0275
s0 = 100
v0 = 1
T = 1
sigma = 0.2
kappa = 4
theta = 0.02
rho = 3
v_0 = 0.02
xi = 0.9


M = Market(n=n, paths=N, r=r, s0=s0, time_horizon=T)

#S = M.black_scholes(sigma=sigma)
S = M.heston_paths(kappa=kappa, theta=theta, v_0=v0, rho=rho, xi=xi, return_vol=False)
t = M.time_grid()
for j in range(N):
    plt.plot(t, S[j, :])

#plt.plot(t,S[0,:])
plt.show()