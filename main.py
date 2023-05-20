import numpy as np
import matplotlib.pyplot as plt
from market import Market
from options import value_fun


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
call = value_fun().Call(K=K)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()
Option_value = np.array(list(map(call,Stock)))

for i in range(N):
    plt.plot(t,Stock[i,:])
plt.legend()
plt.show()