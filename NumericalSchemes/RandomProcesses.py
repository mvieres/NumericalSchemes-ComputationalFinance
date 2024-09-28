import numpy as np

import NumericalSchemes.TimeGrid as TimeGrid
import NumericalSchemes.Utils as Utils


class RandomProcesses:

    @staticmethod
    def brownian_motion_path(time_grid_instance: TimeGrid, n_steps: int, dimension: int, starting_point=None,
                             correlation_matrix=None, seed=None) -> np.array:
        """
        Create a Brownian motion path for a given time grid. If the time grid instance is not yet defined, equidistant
        is chosen.
        @param time_grid_instance:
        @param n_steps:
        @param dimension:
        @param starting_point:
        @param correlation_matrix:
        @return:
        """
        assert n_steps >= 1
        assert len(starting_point) > 1 if correlation_matrix is not None else True
        if correlation_matrix is not None:
            assert len(starting_point) == len(correlation_matrix), \
                "Dimension of starting point and correlation matrix must be equal"
        if starting_point is not None:
            assert isinstance(starting_point, list) or starting_point is float, "Starting point must be a list or a float"
            matrix = np.linalg.cholesky(correlation_matrix)
        else:
            matrix = np.eye(dimension)
        brownian_motion = Utils.Utils.initForProcesses(dimension, n_steps)
        if starting_point is not None:
            brownian_motion[0] = starting_point
        if seed is not None:
            np.random.seed(seed)

        for i in range(1, n_steps):  # Loop over time steps
            dt = time_grid_instance.get_dt_diff_to_previous_point(n_steps, i)
            if dimension > 1:
                brownian_motion[i] = brownian_motion[i - 1] + np.sqrt(dt) * (matrix @ np.random.normal(size=dimension))
            else:
                brownian_motion[i] = brownian_motion[i - 1] + np.sqrt(dt) * np.random.normal()
        return brownian_motion

    @staticmethod
    def brownian_bridge(time_grid_instance: TimeGrid, n_steps1: int, n_steps2: int) -> np.array:
        pass

    @staticmethod
    def multiple_brownian_motion_paths(time_grid_instance: TimeGrid, n_paths: int, n_steps: int, dimension: int,
                                       starting_point=None, correlation_matrix=None) -> np.array:
        """
        Create multiple Brownian motion paths
        @param time_grid_instance:
        @param n_paths:
        @param n_steps:
        @param dimension:
        @param starting_point:
        @param correlation_matrix:
        @return:
        """
        brownian_motion_paths = {}
        for numberPath in range(n_paths):
            brownian_motion_paths[numberPath] = RandomProcesses.brownian_motion_path(time_grid_instance, n_steps,
                                                                                     dimension, starting_point,
                                                                                     correlation_matrix)
        return brownian_motion_paths

    @staticmethod
    def geometric_brownian_motion_exact(timeGridInstance: TimeGrid, nSteps: int, startingPoint: float, drift: float,
                                        diffusion: float, seed: int = None) -> np.array:
        """
        Create a one dimensional geometric Brownian motion path
        @param timeGridInstance:
        @param nSteps:
        @param startingPoint:
        @param drift:
        @param diffusion:
        @param seed:
        @return:
        """
        assert nSteps >= 1, "Number of steps must be greater than 1"
        assert diffusion >= 0, "Diffusion must be non negative"
        if seed is not None:
            np.random.seed(seed)
        timeGrid = timeGridInstance.get_time_grid(nSteps)
        gbm = np.zeros((nSteps, 1))  # TODO: this might be the wrong shape
        for i in range(0, nSteps):
            gbm[i] = startingPoint*np.exp((drift - 0.5*diffusion**2)*timeGrid[i]
                                          + diffusion*np.sqrt(timeGrid[i])*np.random.normal())
        return gbm

    @staticmethod
    def multiple_geometric_brownian_motion_exact_paths(timeGridInstance: TimeGrid, nPaths: int, nSteps: int,
                                                       startingPoint: float, drift: float, diffusion: float,
                                                       seed: int = None) -> np.array:
        """
        Create multiple geometric Brownian motion paths
        @param timeGridInstance:
        @param nPaths:
        @param nSteps:
        @param startingPoint:
        @param drift:
        @param diffusion:
        @param seed:
        @return:
        """
        gbmPaths = {}
        for numberPath in range(nPaths):
            gbmPaths[numberPath] = RandomProcesses.geometric_brownian_motion_exact(timeGridInstance, nSteps, startingPoint,
                                                                                   drift, diffusion, seed)
        return gbmPaths