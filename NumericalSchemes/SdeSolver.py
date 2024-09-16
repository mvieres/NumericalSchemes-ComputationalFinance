import numpy as np

import NumericalSchemes.RandomProcesses as RP
import NumericalSchemes.TimeGrid as TimeGrid
import NumericalSchemes.Utils as Utils


class SdeSolver:

    """
    General setting: dX(t) = mu(t, X(t))dt + sigma(t, X(t))dW(t) can be solved by different numerical schemes.
    X(t) is the multidimensional state variable. mu(t, X(t)) is the drift term. sigma(t, X(t)) is the diffusion term.
    Dirft and diffusion terms are given as a dictionary with keys as dimension-index ans values as lambda functions with
    respect to time and state.
    To reflect a general multidimensional setting,


    The following numerical schemes are implemented: Euler, Absolute Euler, Milstein
    TODO: Alfonsi Scheme, Drift Implicit Euler, Full implicit euler
    TODO: Inconsistency for dimension within dict and callable drift and diffusion
    """
    # TODO: Adapt to general time grid use, fix init for dimension and starting points.

    def __init__(self, time_grid_instance: TimeGrid, drift: callable or dict, diffusion: callable or dict,
                 starting_point: np.array or float, order_dimensions=None):
        self.time_grid_instance = time_grid_instance
        self.dimension = None
        self.drift = drift
        self.diffusion = diffusion
        self.starting_point = starting_point
        self.dimension = self.get_dimension(starting_point)
        self.order_dimensions = order_dimensions
        if order_dimensions is not None:
            assert isinstance(order_dimensions, list), "Order dimensions must be a list"
        else:
            self.order_dimensions = list(range(1, self.dimension, 1))  # TODO: check this
        if isinstance(drift, dict) and isinstance(diffusion, dict):
            self.one_dimensional = False
        elif callable(drift) and callable(diffusion):
            self.one_dimensional = True
        else:
            raise ValueError("Input error: Drift and diffusion have to be either callable or dict")
        pass

    def set_order(self, order_dimensions: list) -> None:
        self.order_dimensions = order_dimensions

    def get_dimension(self, starting_point) -> int:
        if isinstance(starting_point, float) or isinstance(starting_point, int):
            dim = 1
        else:
            dim = len(starting_point)
        return dim

    def calculate_diffusion_euler(self, dimension: int, bm_increment, time, space):
        diffusion_vector = self.diffusion[dimension]
        diffusion_keys = diffusion_vector.keys()
        diffusion_evaluated = 0
        for key in diffusion_keys:
            diffusion_evaluated += (diffusion_vector[key](time, space)*bm_increment[key-1])
        return diffusion_evaluated

    def init_for_schemes(self, n_steps: int, bm_path=None, starting_point=None):
        assert n_steps > 1, "nSteps has to be bigger than 1"
        timeGrid = self.time_grid_instance.get_time_grid(n_steps)
        if bm_path is None:
            bm_path = RP.RandomProcesses.brownian_motion_path(time_grid_instance=self.time_grid_instance,
                                                              n_steps=n_steps, dimension=self.dimension)
        if starting_point is not None:
            self.starting_point = starting_point  # Update new starting point
            self.dimension = self.get_dimension(starting_point)
        else:
            starting_point = self.starting_point
        x = Utils.Utils.initForProcesses(self.dimension, n_steps)
        x[0] = starting_point  # initial condition
        return timeGrid, bm_path, x

    def euler_1d(self,n_steps, time_grid, bm_path, x):
        for i in range(1, n_steps):
            x[i] = (x[i - 1] + self.drift(time_grid[i - 1], x[i - 1]) * (time_grid[i] - time_grid[i - 1])
                    + self.diffusion(time_grid[i - 1], x[i - 1]) * (bm_path[i] - bm_path[i - 1]))
        return x

    def euler_multi_d(self, n_steps, time_grid, bm_path, x):
        for i in range(1, n_steps):
            for dimension in self.order_dimensions:  # TODO: make sure order_dimension works here
                dim_index = dimension - 1
                x[i][dim_index] = (x[i - 1][dim_index] + self.drift[dimension](time_grid[i - 1], x[i - 1]) * (time_grid[i] - time_grid[i - 1]) + self.calculate_diffusion_euler(dimension, bm_path[i] - bm_path[i - 1], time_grid[i - 1], x[i - 1]))
        return x

    def euler(self, n_steps: int, starting_point=None, bm_path=None) -> np.array:
        """
        Euler Scheme for multidimensional stochastic differential equations. Drift and diffusion have to be given as

        @param time_grid_instance:
        @param n_steps:
        @param starting_point:
        @param drift:
        @param diffusion:
        @param order_dimensions: Dimensions in which the Euler scheme is to be applied
        @return:
        """
        time_grid, bm_path, x = self.init_for_schemes(n_steps, bm_path, starting_point)
        if not self.one_dimensional:
            x = self.euler_multi_d(n_steps, time_grid, bm_path, x)
        else:
            x = self.euler_1d(n_steps, time_grid, bm_path, x)
        return x

    def absolut_euler_1d(self, n_steps, time_grid, bm_path, x):
        for i in range(1, n_steps):
            x[i] = (x[i - 1] + np.abs(self.drift(time_grid[i - 1], x[i - 1]) * (time_grid[i] - time_grid[i - 1])
                    + self.diffusion(time_grid[i - 1], x[i - 1]) * (bm_path[i] - bm_path[i - 1])))
        return x

    def absolute_euler_multi_d(self, n_steps, time_grid, bm_path, x):
        for i in range(1, n_steps):
            for dimension in self.order_dimensions: # TODO: make sure order_dimension works here
                dim_index = dimension - 1
                x[i][dim_index] = (x[i - 1][dim_index] + np.abs(self.drift[dimension](time_grid[i - 1], x[i - 1]) * (time_grid[i] - time_grid[i - 1]) + self.calculate_diffusion_euler(dimension, bm_path[i] - bm_path[i - 1], time_grid[i - 1], x[i - 1])))
        return x

    def absolute_euler(self, n_steps: int, startingPoint=None):
        time_grid, bm_path, x = self.init_for_schemes(n_steps, startingPoint)
        if not self.one_dimensional:
            x = self.absolute_euler_multi_d(n_steps, time_grid, bm_path, x)
        else:
            x = self.absolut_euler_1d(n_steps, time_grid, bm_path, x)
        return x

    def check_for_constant_diffusion(self):
        for dimension in self.order_dimensions:
            diffusion_vector = self.diffusion[dimension]
            diffusion_keys = diffusion_vector.keys()
            for key in diffusion_keys:
                assert diffusion_vector[key](2, 2) == diffusion_vector[key](1, 1), "Diffusion is not constant"
        pass

    def drift_implicit_euler(self, nSteps: int, startingPoint=None):
        time_grid, bm_path, x = self.init_for_schemes(nSteps, startingPoint)
        self.check_for_constant_diffusion()
        # TODO
        if not self.one_dimensional:
            pass
        else:
            pass
        return x

    def set_diffustion_derivative(self, diffusion: dict or callable):
        if isinstance(diffusion, dict):
            self.diffusion_derivative = diffusion
        elif callable(diffusion):
            self.diffusion_derivative = diffusion
        else:
            raise ValueError("Diffusion derivative has to be either callable or dict")

    def milstein(self, nSteps: int, startingPoint=None) -> np.array:
        time_grid, bm_path, x = self.init_for_schemes(nSteps, startingPoint)
        if not self.one_dimensional:
            pass  # TODO
        else:
            assert callable(self.diffusion_derivative), "Diffusion derivative has to be callable"
            for i in range(1, nSteps):
                delta_t = time_grid[i] - time_grid[i-1]
                x[i] = (x[i - 1] + self.drift(time_grid[i - 1], x[i - 1]) * delta_t +
                        self.diffusion(time_grid[i - 1], x[i - 1]) * (bm_path[i] - bm_path[i - 1])
                        + 0.5 * self.diffusion(time_grid[i - 1], x[i - 1]) *
                        self.diffusion_derivative(time_grid[i - 1], x[i - 1]) *
                        ((bm_path[i] - bm_path[i - 1]) ** 2 - delta_t))
        return x

    def leapfrog(self):
        # TODO: sheet 07 ex 3 num_sde
        pass