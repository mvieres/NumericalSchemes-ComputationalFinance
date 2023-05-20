import numpy as np

from market import Market
from algo import LSM
from options import value_fun_x

T = 1
N = 3
n = 10

degree = 5

r = 0.01
sigma = 0.5
s0 = 1
M = Market(n=n,N=N,sigma=sigma,r=r,s0=s0,T=T)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()


LSM(Market,degree)