import numpy as np

class Market:
    """ Creates the market environment.
        Works for Models driven by a 1-dimensional Brownian Motion.
    """

    def __init__(self, n, paths, sigma, r, s0, time_horizon):
        try:
            assert n > 0
            self.n = int(n)
            assert paths > 0
            self.N = int(paths)
            assert sigma >= 0
            self.sigma = float(sigma)
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

    def black_scholes(self):
        """ Creates the Black Scholes Model using the closed Formula
            s(t) = s_0* exp( (r - 0.5*sigma^2)*t + sigma*W_t)

        Returns:
            s (Matrix / Array): Asset price (row -> Samples, columns -> time points)
        """
        t = self.time_grid()
        bb = self.brownian_motion()
        s = np.zeros(shape=(self.N, self.n))
        for j in range(self.N):
            for i in range(self.n):
                s[j, i] = self.s0 * np.exp((self.r - 0.5 * (self.sigma ** 2)) * t[i] + self.sigma * bb[j, i])
        return s

