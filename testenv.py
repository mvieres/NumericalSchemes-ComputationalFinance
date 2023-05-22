import numpy as np
import matplotlib.pyplot as plt
from functions import Market

n = 252
N = 1
r = 0.05
s0 = 100
T = 1
sigma = 0.2

M = Market(N=N, n=n, sigma=sigma, r=r, s0=s0, T=T)

S = M.brownian_motion()
t = M.time_grid()
#for j in range(N):
    #plt.plot(t,S[j,:])





plt.plot(t,S[0,:])

plt.show()