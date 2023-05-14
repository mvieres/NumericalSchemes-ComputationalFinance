import numpy as np
import matplotlib.pyplot as plt
from functions import brownian_motion, black_scholes


T=1 # Time horizon
n=100000 # Discretization number per time unit
N = 10 # Number of paths
delta_t = T/n
time = np.linspace(0,1,n)
BB = brownian_motion(n=n,N=N)
BS = black_scholes(2,3,1,N,n)

for i in range(N):
    plt.plot(time,BS[i,])
plt.legend()
plt.show()