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


    The following numerical schemes are implemented:

    """
    @staticmethod
    def euler(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array or float,
              drift: dict or callable, diffusion: dict or callable, orderDimensions=None) -> np.array:
        """
        Euler Scheme for multidimensional stochastic differential equations. Drift and diffusion have to be given as

        @param timeGridInstance:
        @param nSteps:
        @param startingPoint:
        @param drift:
        @param diffusion:
        @param orderDimensions: Dimensions in which the Euler scheme is to be applied
        @return:
        """
        assert nSteps > 1, "nSteps has to be bigger than 1"
        bb = RP.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        delta_t = timeGrid[1] - timeGrid[0]
        x = Utils.Utils.initForProcesses(startingPoint, nSteps)
        x[0] = startingPoint  # initial condition
        if orderDimensions is not None:
            for i in range(1, nSteps):
                for dimension in orderDimensions:
                    x[i, dimension] = (x[i - 1, dimension] + drift[dimension](timeGrid[i - 1], x[i - 1]) * delta_t
                                      + diffusion[dimension](timeGrid[i - 1], x[i - 1]) * (bb[i] - bb[i - 1]))
        else:
            for i in range(1, nSteps):
                x[i] = (x[i - 1] + drift(timeGrid[i - 1], x[i - 1]) * delta_t
                        + diffusion(timeGrid[i - 1], x[i - 1]) * (bb[i] - bb[i - 1]))
        return x

    @staticmethod
    def absoluteEuler(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array,
                      drift: callable, diffusion: callable) -> np.array:
        bb = RP.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        delta_t = timeGrid[1] - timeGrid[0]
        x = np.zeros((nSteps, len(startingPoint)))  # array to store the solution
        x[0] = startingPoint  # initial condition
        for i in range(1, nSteps):
            x[i] = x[i - 1] + np.abs(drift(timeGrid[i - 1], x[i - 1]) * delta_t + diffusion(timeGrid[i - 1], x[i - 1])
                                     * (bb[i] - bb[i - 1]))
        return x

    @staticmethod
    def implicitEuler(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array, drift: callable, diffusion: callable):
        pass

    @staticmethod
    def milstein(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array, drift: callable, diffusion: callable,
                 diffusionDerivative: callable) -> np.array:
        bb = RP.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        delta_t = timeGrid[1] - timeGrid[0]
        x = np.zeros((nSteps, len(startingPoint)))  # array to store the solution
        x[0] = startingPoint  # initial condition
        for i in range(1, nSteps):
            x[i] = (x[i - 1] + drift(timeGrid[i - 1], x[i - 1]) * delta_t + diffusion(timeGrid[i - 1], x[i - 1]) *
                    (bb[i] - bb[i - 1]) + 0.5 * diffusion(timeGrid[i - 1], x[i - 1]) *
                    diffusionDerivative(timeGrid[i - 1], x[i - 1]) * ((bb[i] - bb[i - 1]) ** 2 - delta_t))
        return x
