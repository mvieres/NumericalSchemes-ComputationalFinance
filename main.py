import numpy as np
import matplotlib.pyplot as plt
from market import Market
from options import value_fun_x


T=1 # Time horizon
n=1000 # Discretization number per time unit
N = 5 # Number of paths
sigma = 0.5
s0 = 1
r= 0.05
K = 1
delta_t = T/n

#BB = Market.brownian_motion(n=n,N=N)
M = Market(n=n,N=N,sigma=sigma,r=r,s0=s0,T=T)

t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()
Option_payoff = np.zeros_like(Stock)
for i in range(N):
    for j in range(n):
        Option_payoff[i,j] = value_fun_x().Call(x = Stock[i,j],K=K)

for i in range(N):
    plt.plot(t,Stock[i,:])
    #plt.plot(t, Option_payoff[i,:])
plt.legend()
plt.show()