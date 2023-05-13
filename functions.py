import numpy as np  


def brownian_motion(N,T):
    # Create normal distributed random numbers by using random.normal
    mu, sigma = 0, np.sqrt(1/N) # Mean and standard deviation 
    s = np.random.normal(mu, sigma, N*T) # N*T normal distributed random numbers 

    # Construct realization of Brownian Motion 
    B=np.zeros(N*T+1)  # Vector creation
    for i in range(N*T):
        B[i+1]=B[i]+s[i] # Summig the increments of BM on each time step
    return B

