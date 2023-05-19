import numpy as np

from market import Market
from options import value_fun

def LSM(Market,v):
    
    Stock = Market.black_scholes()
    t = Market.time_grid()
    m = len(Stock, axis = 1)
    n = len(t)
    
    C = np.zeros(shape=(m,n))
    S = np.zeros(shape=(m,n))
    
    for j in range(m):
        if v(Stock[j,n]):
            S[j,n] = 1
    
    for j in range(m):
        C[j,n] = v(Stock[j,n])
    
    
    for j in range(m, 2, -1):
        U = np.zeros(shape=(m,))
        z = 1
        Xtemp = np.array([])
        Ytemp = np.array([])
        
    