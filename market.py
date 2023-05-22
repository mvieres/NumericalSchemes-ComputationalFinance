import numpy as np  

class Market():
    """ Creates the market environment.
        Works for Models driven by a 1-dimensional Brownian Motion.
    """
    def __init__(self,n,N,sigma,r,s0,T):
        self.n = n
        self.N = N
        self.sigma = sigma
        self.r = r
        self.s0 = s0
        self.T = T
        
   
        
    def brownian_motion(self):
        """Computes #N Sample paths of brownian motion

        Args:
            n (int): total number of grid points --> look time_grid()
            N (int): total Number of Samples drawn
        """

        #np.random.seed(42)
        
        t = self.time_grid()
        delta_t = t[1] - t[0]
        dB = np.sqrt(delta_t) * np.random.normal(size=(self.N,self.n - 1))
        B0 = np.zeros(shape=(self.N,1))
        B = np.concatenate((B0,np.cumsum(dB,axis=1)),axis= 1)
        return B
    
    def black_scholes(self):
        """ Creates the Black Scholes Model using the closed Formula
            S(t) = s_0* exp( (r - 0.5*sigma^2)*t + sigma*W_t)

        Returns:
            S (Matrix / Array): Assetprice (row -> Samples, columns -> time points)
        """
        t = self.time_grid()
        BB = self.brownian_motion()
        S = np.zeros(shape=(self.N,self.n))
        for j in range(self.N):
            for i in range(self.n):
                S[j,i] = self.s0*np.exp((self.r - 0.5*(self.sigma**2))*t[i] + self.sigma*BB[j,i])
        return S
    
    def bs_phi(self,t,x):
        """performs transformation for time variable t and space Variable x of Geometric brownian Motion
            --> Primarily used for Antithetic Monte Carlo Estimation of Geometric Asian Call
        Args:
            t (float): time point
            x (float): space point
        """
        return self.s0*np.exp((self.r - 0.5*self.sigma**2)*t + self.sigma*x)
    
    def time_grid(self):
        """Creats a time grid given Time Horizon T and total number of points n.

        Returns:
            Vector / array: time points
        """
        time = np.linspace(0,self.T,self.n)
        return time
