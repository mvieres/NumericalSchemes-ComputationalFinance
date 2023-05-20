import numpy as np

from market import Market
from options import value_fun_x as vfun


# Aufpassen wie v supplied wird --> aktuell from 


#
def LSM(Market,v,degree):

    Stock = Market.black_scholes()
    t = Market.time_grid()
    m = len(Stock, axis = 1)
    n = len(t)
    r = Market.r
    
    C = np.zeros(shape=(m,n))
    S = np.zeros(shape=(m,n))
    
    for j in range(m):
        if vfun.v(Stock[j,n]):
            S[j,n] = 1
    
    for j in range(m):
        C[j,n] = vfun.v(Stock[j,n])
    
    
    for j in range(m, 2, -1):
        U = np.zeros(shape=(m,))
        z = 1
        Xtemp = np.array([])
        Ytemp = np.array([])
        for i in range(m):
            if vfun.v(Stock[i,j-1]) > 0:
                U[i] = 1
                val = np.array(np.sum([C[i,k]+np.exp(-r*(t[k+1]-t[k])) for k in range(j,n+1)]))
                Ytemp = np.append(Ytemp, val)
                Xtemp = np.append(Xtemp, Stock[i,j-1])
    X = Xtemp
    Y = Ytemp
    regression = np.polyfit(X,Y,degree)
    Xcont = np.polyval(regression, Stock[:,j])
    Xex = np.array([vfun.v(X[_]) for _ in range(X)])
    
    z = 0
    for i in range(m):
        if U[i] == 1:
            if Xex[z] < Xcont[z]:
                for k in range(j,n): # n Evnetuell falsch
                    C[i,k] = S[i,k]*vfun.v(Stock[i,k])
            else:
                S[i, j-1] = 1
                S[i, j in range(n)] = 0
                C[i, j-1] = vfun.v(Stock[i,j-1])# U.u viele indexfehler
                C[i, j in range(n)] = 0
        z = z+1
        
