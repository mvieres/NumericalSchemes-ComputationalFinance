import numpy as np
import matplotlib.pyplot as plt
from functions import Market


T=1 # Time horizon
n=1000 # Discretization number per time unit
N = 5 # Number of paths
sigma = 3
mu = 0.5
s0 = 1
r= 0.01
delta_t = T/n

#BB = Market.brownian_motion(n=n,N=N)
M = Market(n=n,N=N,sigma=sigma,mu=mu,r=r,s0=s0,T=T)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()
for i in range(N):
    plt.plot(t,Stock[i,:])
plt.legend()
plt.show()