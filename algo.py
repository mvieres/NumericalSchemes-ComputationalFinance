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
        if vfun().Put(x = Stock[j,n-1],K=K)>0:
            S[j,n-1] = 1
    
    for j in range(m):
        C[j,n-1] = vfun().Put(x= Stock[j,n-1],K=K)
    
    
    for j in range(n-1, 3, -1):
        print(j)
        U = np.zeros(shape=(m,))
        z = 0 
        Xtemp = np.array([])
        Ytemp = np.array([])
        for i in range(m):
            if vfun().Put(x = Stock[i,j-1],K=K) > 0:
                U[i] = 1
                val = np.array(np.sum([C[i,k]+np.exp(-r*(t[k+1]-t[k])) for k in range(j,n-1)]))
                Ytemp = np.append(Ytemp, val)
                Xtemp = np.append(Xtemp, Stock[i,j-1])
                z = z + 1
    

        X = Xtemp
        Y = Ytemp
        regression = np.polyfit(X,Y,degree)
        Xcont = np.polyval(regression, Stock[:,j])
        Xex = np.array([vfun().Put(x = X[_],K=K) for _ in range(len(X))])
        
        
        for i in range(m):
            
            z = 0 # Nicht klar wo dieses Init hingehoert
            if U[i] == 1: # Checkin for in the money path
                if Xex[z] < Xcont[z]:
                    for k in range(j,n): # n Evnetuell falsch
                        C[i,k] = S[i,k]*vfun().Put(x = Stock[i,k],K=K)
                else:
                    S[i, j-1] = 1
                    S[i, j in range(n)] = 0
                    C[i, j-1] = vfun().Put(x = Stock[i,j-1],K=K)# U.u viele indexfehler
                    C[i, j in range(n)] = 0
            z = z+1
    
    # Monte Carlo (?)
    Value = np.sum(np.sum(C*np.exp(-r+delta_t),axis=1),axis=0)/m
    #TODO: Strategy
    return Value, S, C
        


def Call(x,K): 
        
    return np.maximum(0, x - K)
    
def Put(x,K):
    return np.maximum(0, K - x)


def longstaff_schwartz(Market, degree, K):
    """Performs the Least squares Monte Carlo Estimation for American Put(!!) Options. Uses Black Scholes Model as underlying Market Model

    Args:
        Market (Array): on axis 0: Sample paths, on axis 1 values at each time point for a given Samplepatz
        degree (int): Maximum polynomial degree to be considered for regression
        K (float): strike price
    Returns:
        float: Estimated value of american Option
    """
    
    # Extracting t, S from Market environment
    t = Market.time_grid()
    S = Market.black_scholes()
    r = Market.r
    
    #
    delta_t = t[1] - t[0]
    num_steps = t.shape[0] # Number of time steps (soldimensions)
    num_mc = S.shape[0] # Number of monte carlo runs (rowdimensions)
    
    
    discont = np.exp(-r*delta_t) # Constant discount factor, because grid is equidistant
   
    # Preallocation Continuation Value, i.e Z_{\tau_{j+1}}
    contin_val = np.zeros_like(S)
    
    # Allocate last time point, i.e. Exercise value of Option
    for j in range(num_mc):
        contin_val[j,-1] = Put(S[j,-1],K=K)
    
    # Iteration backwards in Time
    for t in range(num_steps - 2, 1, -1):
        reg = np.polyfit(S[:,t], contin_val[:,t+1]*discont, deg=degree)
        contin_val[:,t] = np.polyval(reg,S[:,t])
        
        # Exercise value
        ex_val = np.zeros_like(S[:,t])
        for j in range(num_mc):
            ex_val[j] = Put(S[j,t],K=K)
        
        ex_itm = np.where(ex_val > contin_val[:,t])[0] # Comparing exercise and continuation value
        
        # Update Continuation value
        for j in ex_itm:
            contin_val[j,t] = Put(S[j,t],K=K)
            contin_val[j, t+1] = 0
        
        # Standard Monte Carlo 
        value = np.mean(np.sum(contin_val*discont,axis = 1))
        
    return value
        

        
        
    