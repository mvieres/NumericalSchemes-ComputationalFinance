import numpy as np
import matplotlib.pyplot as plt

from market import Market
from algo import longstaff_schwartz, LSM


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

#Value = np.zeros(shape=(2,))

#Value = longstaff_schwartz(Market= M,degree = degree,K = 45)
 
K = np.linspace(1,100,100)
res_value = np.zeros_like(K)  
var = np.zeros_like(K)

z= 0 
for k in K:
    print(k)
    res_value[z], var[z] = longstaff_schwartz(Market= M,degree = degree,K = k,payoff = "Call")
    #res_value[z] = LSM(Market=M,degree=degree,K=k)
    z = z+1

plt.plot(K,res_value)
plt.title('LSM with 1000 MC Runs and Gridsize 100, s0 = 36')
plt.axvline(s0,color = 'red')
plt.xlabel('Strike price K')
plt.ylabel('Estimated v_0')
plt.savefig('picture.png')
plt.show()