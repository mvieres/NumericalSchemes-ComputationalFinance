import numpy as np

import NumericalSchemes.RandomProcesses as randomProcesses
import NumericalSchemes.TimeGrid as TimeGrid


class SdeSolver:

    @staticmethod
    def euler(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array, drift: callable, diffusion: callable) -> np.array:
        bb = randomProcesses.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        delta_t = timeGrid[1] - timeGrid[0]
        x = np.zeros((nSteps, len(startingPoint)))  # array to store the solution
        x[0] = startingPoint  # initial condition
        for i in range(1, nSteps):
            x[i] = (x[i - 1] + drift(timeGrid[i - 1], x[i - 1]) * delta_t
                    + diffusion(timeGrid[i - 1], x[i - 1]) * (bb[i] - bb[i - 1]))
        return x

    @staticmethod
    def absoluteEuler(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array, drift: callable, diffusion: callable) -> np.array:
        bb = randomProcesses.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
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
    def milstein(timeGridInstance: TimeGrid, nSteps: int, startingPoint: np.array, drift: callable, diffusion: callable, diffusionDerivative: callable) -> np.array:
        bb = randomProcesses.RandomProcesses.brownianMotionPath(timeGridInstance, nSteps, startingPoint)
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        delta_t = timeGrid[1] - timeGrid[0]
        x = np.zeros((nSteps, len(startingPoint)))  # array to store the solution
        x[0] = startingPoint  # initial condition
        for i in range(1, nSteps):
            x[i] = (x[i - 1] + drift(timeGrid[i - 1], x[i - 1]) * delta_t + diffusion(timeGrid[i - 1], x[i - 1]) *
                    (bb[i] - bb[i - 1]) + 0.5 * diffusion(timeGrid[i - 1], x[i - 1]) *
                    diffusionDerivative(timeGrid[i - 1], x[i - 1]) * ((bb[i] - bb[i - 1]) ** 2 - delta_t))
        return x