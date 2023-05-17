import numpy as np
import scipy as sc
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
        