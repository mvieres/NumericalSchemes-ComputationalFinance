import numpy as np  


def brownian_motion(n,N):
    """Computes #N Sample paths of brownian motion

    Args:
        n (_type_): _description_
        N (_type_): _description_
    """
    delta_t = 1/n
    mu, sigma = 0, np.sqrt(delta_t)
    B = np.zeros(shape=(N,n+1))
    for j in range(N):
        Rv = np.random.normal(mu,sigma, n)
        for i in range(n):
            B[j,i+1] = B[j,i] + Rv[i]
    return B


def black_scholes(sigma,mu,s0,N,n):
    time = np.linspace(0,1,n+1)
    BB = brownian_motion(n,N)
    S = np.zeros(shape=(N,n))
    for j in range(N):
        for i in range(n):
            S[j,i] = s0*np.exp((mu - 0.5*(sigma**2))*time[i] + sigma*BB[j,i])
    return S