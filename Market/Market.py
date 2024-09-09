import numpy as np
import matplotlib.pyplot as plt
from NumericalSchemes.TimeGrid import TimeGrid


class Market:
    """
    This class assumes a constant risk-free return rate of the money market account at first.
    For the given timegrid, the risk-free rate can be evaluated at tenor points. TODO: This is not yet implemented
    """
    def __init__(self, tStart: float, tEnd: float, s0: float, r: float or None):
        """
        :param tStart: float, start time
        :param tEnd: float, end time
        :param s0: float, initial stock price
        :param r: float, risk-free rate, this will be the constant risk-free return rate of the money market account
        """
        assert tStart < tEnd, "Start time must be less than end time"
        assert s0 > 0, "Initial stock price must be positive"
        assert r >= 0, "Risk-free rate must be non negative"
        assert s0 > 0, "Initial stock price must be positive"
        self.t_start = tStart
        self.t_end = tEnd
        self.time_grid_instance = TimeGrid(tStart, tEnd)
        self.s0 = s0
        self.r = r
        self.underlying = {}
        self.dimension = None
        pass

    def reset(self):
        self.__init__(self.t_start, self.t_end, self.s0, self.r)

    def get_short_rate(self):
        return self.r

    def compute_solution_path(self, n_steps: int) -> np.array:
        pass

    def plot_underlying(self):
        keys_underlying = self.underlying.keys()
        time_grid = self.time_grid_instance.get_time_grid(len(self.underlying[list(keys_underlying)[0]]))

        if self.dimension == 1:
            for key in keys_underlying:
                plt.plot(time_grid, self.underlying[key], label=key)
        elif self.dimension == 2:
            for key in keys_underlying:
                spot = np.zeros(len(time_grid))
                for i in range(len(time_grid)):
                    spot[i] = self.underlying[key][i][0]
                plt.plot(time_grid, list(spot), label=key)
        else:
            raise ValueError("Something went wrong with the implementation")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.show()
