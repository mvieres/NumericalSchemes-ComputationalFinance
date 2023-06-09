import numpy as np
import matplotlib.pyplot as plt
from functions import Market

n = 1000
N = 10
r = 0.0275
s0 = 100
T = 1
sigma = 0.2

M = Market(N=N, n=n, sigma=sigma, r=r, s0=s0, T=T)

S = M.black_scholes()
t = M.time_grid()
for j in range(N):
    plt.plot(t, S[j, :])



#plt.plot(t,S[0,:])

plt.show()