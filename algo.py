import numpy as np

from options import value_fun_x as vfun


#
def LSM(Market,degree,K):

    Stock = Market.black_scholes()
    t = Market.time_grid()
    m = Market.N
    n = Market.n
    r = Market.r
    
    delta_t = t[-1] - t[-2]
    C = np.zeros(shape=(m,n))
    S = np.zeros(shape=(m,n))
    
    for j in range(m):
        if vfun().Call(x = Stock[j,n-1],K=K):
            S[j,n-1] = 1
    
    for j in range(m):
        C[j,n-1] = vfun().Call(x= Stock[j,n-1],K=K)
    
    
    for j in range(n-1, 3, -1):
        print(j)
        U = np.zeros(shape=(m,))
        z = 0 
        Xtemp = np.array([])
        Ytemp = np.array([])
        for i in range(m):
            if vfun().Call(x = Stock[i,j-1],K=K) > 0:
                U[i] = 1
                val = np.array(np.sum([C[i,k]+np.exp(-r*(t[k+1]-t[k])) for k in range(j,n-1)]))
                Ytemp = np.append(Ytemp, val)
                Xtemp = np.append(Xtemp, Stock[i,j-1])
                z = z + 1
    

        X = Xtemp
        Y = Ytemp
        regression = np.polyfit(X,Y,degree)
        Xcont = np.polyval(regression, Stock[:,j])
        Xex = np.array([vfun().Call(x = X[_],K=K) for _ in range(len(X))])
        
        
        for i in range(m):
            
            z = 0 # Nicht klar wo dieses Init hingehoert
            if U[i] == 1: # Checkin for in the money path
                if Xex[z] < Xcont[z]:
                    for k in range(j,n): # n Evnetuell falsch
                        C[i,k] = S[i,k]*vfun().Call(x = Stock[i,k],K=K)
                else:
                    S[i, j-1] = 1
                    S[i, j in range(n)] = 0
                    C[i, j-1] = vfun().Call(x = Stock[i,j-1],K=K)# U.u viele indexfehler
                    C[i, j in range(n)] = 0
            z = z+1
    
    # Monte Carlo (?)
    Value = np.sum(np.sum(C*np.exp(-r+delta_t),axis=1),axis=0)/m
    #TODO: Strategy
    return Value, S, C
        
