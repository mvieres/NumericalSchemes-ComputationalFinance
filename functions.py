import numpy as np  


class Market():
    def __init__(self,n,N,sigma,mu,r,s0,T):
        self.n = n
        self.N = N
        self.mu = mu
        self.sigma = sigma
        self.r = r
        self.s0 = s0
        self.T = T
        
    def brownian_motion(self):
        """Computes #N Sample paths of brownian motion

        Args:
            n (_type_): _description_
            N (_type_): _description_
        """
        t = self.time_grid()
        delta_t = t[1] - t[0]
        dB = np.sqrt(delta_t) * np.random.normal(size=(self.N,self.n - 1))
        B0 = np.zeros(shape=(self.N,1))
        B = np.concatenate((B0,np.cumsum(dB,axis=1)),axis= 1)
        return B
    
    def black_scholes(self):
        t = self.time_grid()
        BB = self.brownian_motion()
        S = np.zeros(shape=(self.N,self.n))
        for j in range(self.N):
            for i in range(self.n):
                S[j,i] = self.s0*np.exp((self.mu - 0.5*(self.sigma**2))*t[i] + self.sigma*BB[j,i])
        return S
    
    def time_grid(self):
        time = np.linspace(0,self.T,self.n)
        return time