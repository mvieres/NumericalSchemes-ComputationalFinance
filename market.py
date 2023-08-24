import numpy as np


class Market:
    """ Creates the market environment.
        Works for Models driven by a 1-dimensional Brownian Motion.
    """

    def __init__(self, n, paths, r, s0, time_horizon):
        try:
            assert n > 0
            self.n = int(n)
            assert paths > 0
            self.N = int(paths)
            assert r >= 0
            self.r = float(r)
            self.s0 = float(s0)
            assert time_horizon > 0
            self.T = float(time_horizon)
        except ValueError:
            print('Wrong market parameters')

    def time_grid(self):
        """Creates a time grid given Time Horizon T and total number of points n.

        Returns:
            Vector / array: time points
        """
        time = np.linspace(0, self.T, self.n)
        return time

    def brownian_motion(self):
        """
        Creates the Brownian Motion vector with N sample paths row-wise and n time points column-wise

        Returns:
            bb (Matrix): Brownian motion array
        """
        t = self.time_grid()  # time grid
        delta_t = t[1] - t[0]  # delta t
        db = np.sqrt(delta_t) * np.random.normal(size=(self.N, self.n - 1))  # brownian increments
        b0 = np.zeros(shape=(self.N, 1))  # starting vector
        bb = np.concatenate((b0, np.cumsum(db, axis=1)), axis=1)  # brownian motion
        return bb

    def heston_paths(self, kappa, theta, v_0, rho, xi, return_vol=False):
        dt = self.T / self.n
        size = (self.N, self.n)
        prices = np.zeros(size)
        sigs = np.zeros(size)
        s_t = self.s0
        v_t = v_0
        for t in range(self.n):
            bb = np.random.multivariate_normal(np.array([0, 0]),
                                               cov=np.array([[1, rho],
                                                             [rho, 1]]),
                                               size=self.N) * np.sqrt(dt)

            s_t = s_t * (np.exp((self.r - 0.5 * v_t) * dt + np.sqrt(v_t) * bb[:, 0]))
            v_t = np.abs(v_t + kappa * (theta - v_t) * dt + xi * np.sqrt(v_t) * bb[:, 1])
            prices[:, t] = s_t
            sigs[:, t] = v_t

        if return_vol:
            return prices, sigs
        else:
            return prices

    def black_scholes(self, sigma):
        """

        Parameters
        ----------
        sigma Volatility in Black Scholes SDE

        Returns Black Scholes price Array
        -------

        """
        t = self.time_grid()
        bb = self.brownian_motion()
        s = np.zeros(shape=(self.N, self.n))
        for j in range(self.N):
            for i in range(self.n):
                s[j, i] = self.s0 * np.exp((self.r - 0.5 * (sigma ** 2)) * t[i] + sigma * bb[j, i])
        return s
