import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import longstaff_schwartz


T = 1
N = 1000
n = 100

degree = 5

r = 0.06
sigma = 0.2
s0 = 36


M = Market(n=n,N=N,sigma=sigma,r=r,s0=s0,T=T)
t = M.time_grid()
BB = M.brownian_motion()
Stock = M.black_scholes()
Value, sd, ci = longstaff_schwartz(Market= M,degree = degree,K = 36) 
print(Value)
print(sd)