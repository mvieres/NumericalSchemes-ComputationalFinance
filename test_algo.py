import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import LSM


T = 1
N = 1000
n = 100

degree = 10

r = 0.01
sigma = 0.4
s0 = 5
M = Market(n=n,N=N,sigma=sigma,r=r,s0=s0,T=T)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()

Value = np.zeros(shape=(9,))
for k in range(1, 10, 1):
    Value[k-1], S, C = LSM(Market= M,degree = degree,K = 3)
    
plt.plot(Value)
plt.show()