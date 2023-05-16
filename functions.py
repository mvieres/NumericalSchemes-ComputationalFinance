import numpy as np  
import random as ran
from scipy.linalg import lu
import scipy as sc

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


class European_Options():
    def __init__(self,n,N,K,Assetprice,t):
        """Initialize European Option Class. 
        Goal: Summarize all common European Options within one class for better calling / comparing.

        Args:
            n (Int): Number of time grid points
            N (Int): Number of samples
            K (float): Strike Price (K>0)
            Assetprice (Array): Matrix of Asset prices (axis = 1), Different samples in each row (axis = 0)
            t (Array): time grid
        """
        self.K = K
        self.N = N
        self.n = n
        self.S = Assetprice
        self.t = t
    
    def Arithmetic_asian_call(self,discounted):
        """Computes an European Arithmetic asian Call given the underlying asset S and strike price K

        Returns:
            Vector / Array: Value of the option
        """
        Value = np.zeros(shape = (self.N,))           
        if discounted == True:
            for j in range(self.N):
                Value[j] = np.exp(-self.r*(self.t[-1] -self.t[0]))*np.max((1/self.n)* np.sum(self.S[j,:]) - self.K , 0) 
        else:
            for j in range(self.N):
                Value[j] = np.max((1/self.n)* np.sum(self.S[j,:]) - self.K , 0) 
        return Value
    
    def Call(self,discounted):
        """Computes Standard European Call Option Value at Maturity T for each Sample path (N paths in total).

        Returns:
            Array: Value for each sample path
        """
        Value = np.zeros(shape = (self.N,))

        if discounted == True:
            for j in range(self.N):
                Value[j] = np.exp(-self.r*(self.t[-1] -self.t[0]))*np.max(0, self.S[j,-1] - self.K)
        else:
            for j in range(self.N):
                Value[j] = np.max(0, self.S[j,-1] - self.K)
        return Value

    
    def Put_theory(self,r,sigma):
        pass
        
    def Put(self,discounted):
        """Computes Standard European Put Option Value at Maturity T for each Sample path (N paths in total).

        Returns:
            Array: Value for each sample path
        """
        Value = np.zeros(shape = (self.N,))
        if discounted == True:
            for j in range(self.N):
                Value[j] = np.exp(-self.r*(self.t[-1] -self.t[0]))*np.max(0,  self.K - self.S[j,-1])
        else:
            for j in range(self.N):
                Value[j] = np.max(0,  self.K - self.S[j,-1])
        return Value
    
    def geo_asian_call(self,discounted):
        """Computes an European geometric asian call given the underlying asset S and strike price K

        Returns:
            Array: Value of option
        """
        Value = np.zeros(shape=(self.N,))

        if discounted == True:
            for j in range(self.N):
                Value[j] = np.exp(-self.r*(self.t[-1] - self.t[0]))*np.max(0, (np.prod(self.S)**(1/self.n)) - self.K) 
        else:
            for j in range(self.N):
                Value[j] = np.max(0, (np.prod(self.S)**(1/self.n)) - self.K) 
        return Value
    

class ValueAmerican():
    def __init__(self,n,N,Assetprice,time,v,f,) :
        self.S = Assetprice
        self.t = time
        self.v = v # Soll funktion ein, die value der option berechnet(Input nur Raum Variable!!!)
        self.f = f
        self.n = n
        self.N = N
        self.tau = np.zeros(shape=(N, n)) # Speichert ausuebungsstrategier (Letzte Spalte == 1 beduetet pfad in the money)
        self.C = np.zeros(shape=(self.N,self.n))
        
    def get_Cashflows(self,time):
        """Computes Cashflow of option with value function v at time point 'time'

        Args:
            time (_type_): _description_
        """
        for j in range(self.N):
            self.C[j,time] = self.v(self.S[j,time])
            
    def OLS_MC(self):
        pass

      

# Monte Carlo Methods:
class Monte_Carlo():
    """ Class to perform different Monte Carlo Estimation for financial options
        TODO: Dependencies within init are inconsistent --> Move all non essential (global) variables for each estimator to its respective function
    """
    def __init__(self,N,rv, alpha,r, T,K):
        self.N = N
        self.ov = rv
        self.alpha = alpha
        self.r = r
        self.T = T
        self.K = K
        
        
    def Standard_MC(self):
        """Performs standard Monte Carlo Estimation given N samples of a random variable
            Attention: SMC is 'discounted' with exp(-r*T).
        Returns:
            Float: estimated expected value
            Float: Variance of the estimator
            Array: Confidence Interval
        """
        p_mc = np.exp(-self.r*self.T)*np.mean(self.ov)
        var_mc = np.var(self.ov)
        percentile = sc.stats.norm.ppf(1 - 0.5*self.alpha)
        upper = p_mc + percentile*np.sqrt(var_mc)/self.N
        lower = p_mc - percentile*np.sqrt(var_mc)/self.N
        ki = np.array([lower, upper])
        return p_mc, var_mc, ki
    
    def SMC(self):
        """Performs standard Monte Carlo Estimation given N samples of a random variable

        Returns:
            p_mc (float): Estimated Monte Carlo Value
            var_mc (float): Estimated Monte Carlo Variance of p_mc
            ki (Array): Confidence Interval
        """
        p_mc = np.mean(self.ov)
        var_mc = np.var(self.ov)
        percentile = sc.stats.norm.ppf(1 - 0.5*self.alpha)
        upper = p_mc + percentile*np.sqrt(var_mc)/self.N
        lower = p_mc - percentile*np.sqrt(var_mc)/self.N
        ki = np.array([lower, upper])
        return p_mc, var_mc, ki
    
    def Anti_thetic_MC(self,env):
        """Performs antithetic estimator for geometric brownian motion
        Uses: Environment --> Asset from Market
        Has to be called with r = T and 
        Returns:
            _type_: _description_
        """
        samples = np.zeros(shape=(self.N,))
        const = 0.5*np.exp(-self.r*self.T)
        for j in range(self.N):
            normal_z = np.random.normal(size=(1,))
            samples[j] = const*(np.max(env.bs_phi(self.T,np.sqrt(self.T)*normal_z) - self.K, 0)+ np.max(env.bs_phi(self.T,-1*np.sqrt(self.T)*normal_z) - self.K, 0))
        p_mc = np.mean(samples)
        var_mc = np.var(samples)
        percentile = sc.stats.norm.ppf(1 - 0.5*self.alpha)
        upper = p_mc + percentile*np.sqrt(var_mc)/self.N
        lower = p_mc - percentile*np.sqrt(var_mc)/self.N
        ki = np.array([lower, upper])
        return p_mc, var_mc, ki   
        


def MeanReturn(mat):
    """computes relative mean return of given Sample paths
        (Matrix)
        Each row equals one sample path, e.g. 
    """
    abs_return = np.mean(mat,axis=1) # Axis = 1 import
    relative_return = (abs_return - mat[0,0])/mat[0,0]
    return relative_return