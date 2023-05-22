import numpy as np
import matplotlib.pyplot as plt
from functions import Market

n = 1000
N = 1
r = 1
s0 = 30
T = 1
sigma = 1

M = Market(N=N, n=n, sigma=sigma, r=r, s0=s0, T=T)

S = M.black_scholes()
t = M.time_grid()
#for j in range(N):
    #plt.plot(t,S[j,:])

sigma = np.arange(0.8, 2, 0.2)
z=0
S = np.zeros(shape=(len(sigma),n))
for sig in sigma:
    
    M = Market(N=N, n=n, sigma=sig, r=r, s0=s0, T=T)
    S[z,:] = M.black_scholes()
    z = z+1

t = M.time_grid()
for j in range(6):
    plt.plot(t,S[j,:])
plt.legend(np.round(sigma, 2))
plt.show()