import numpy as np

from market import Market
from algo import LSM


T = 1
N = 4
n = 3

degree = 10

r = 0.01
sigma = 0.5
s0 = 5
M = Market(n=n,N=N,sigma=sigma,r=r,s0=s0,T=T)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()


Value, S, C = LSM(Market= M,degree = degree)
print(Value)