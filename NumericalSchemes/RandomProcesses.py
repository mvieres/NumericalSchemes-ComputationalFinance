import numpy as np

import NumericalSchemes.TimeGrid as TimeGrid
import NumericalSchemes.Utils as Utils


class RandomProcesses:

    @staticmethod
    def brownianMotionPath(timeGridInstance: TimeGrid, nSteps: int, startingPoint: list or float,
                           correlationMatrix=None, seed=None) -> np.array:
        """
        Create a Brownian motion path
        @param timeGridInstance:
        @param nSteps:
        @param startingPoint:
        @param correlationMatrix:
        @param seed:
        @return:
        """
        assert nSteps >= 1
        assert len(startingPoint) > 1 if correlationMatrix is not None else True
        if seed is not None:
            np.random.seed(seed)
        # TODO: assertion for correlationMatrix

        timeGrid = timeGridInstance.getTimeGrid(nSteps)  # TODO: this will not work (wrt the way instances are created)
        delta_t = timeGrid[1] - timeGrid[0]
        bronwianMotion = Utils.Utils.initForProcesses(startingPoint, nSteps)
        bronwianMotion[0] = startingPoint
        if correlationMatrix is not None:
            L = np.linalg.cholesky(correlationMatrix)
            for i in range(1, nSteps):
                bronwianMotion[i] = (bronwianMotion[i - 1] + np.sqrt(delta_t) *
                                     np.dot(L, np.random.normal(size=(len(startingPoint), 1))).T)
        else:
            for i in range(1, nSteps):
                bronwianMotion[i] = (bronwianMotion[i - 1] + np.sqrt(delta_t) *
                                     np.random.normal(size=len(startingPoint)))

        return bronwianMotion

    @staticmethod
    def brownianBridge(timeGridInstance: TimeGrid, nSteps1: int, nSteps2: int) -> np.array:
        pass

    @staticmethod
    def multipleBrownianMotionPaths(timeGridInstance: TimeGrid, nPaths: int, nSteps: int,
                                    startingPoint, correlationMatrix=None) -> np.array:
        """
        Create multiple Brownian motion paths
        @param timeGridInstance:
        @param nPaths:
        @param nSteps:
        @param startingPoint:
        @return:
        """
        bbMotionPaths = {}
        for numberPath in range(nPaths):
             bbMotionPaths[numberPath] = RandomProcesses.brownianMotionPath(timeGridInstance,
                                                                            nSteps, startingPoint, correlationMatrix)
        return bbMotionPaths

    def geometricBrownianMotionExact(timeGridInstance: TimeGrid, nSteps: int, startingPoint: float, drift: float,
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
        timeGrid = timeGridInstance.getTimeGrid(nSteps)
        gbm = np.zeros((nSteps, 1))  # TODO: this might be the wrong shape
        for i in range(0, nSteps):
            gbm[i] = startingPoint*np.exp((drift - 0.5*diffusion**2)*timeGrid[i]
                                          + diffusion*np.sqrt(timeGrid[i])*np.random.normal())
        return gbm

    def multipleGeometricBrownianMotionExactPaths(timeGridInstance: TimeGrid, nPaths: int, nSteps: int,
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
            gbmPaths[numberPath] = RandomProcesses.geometricBrownianMotionExact(timeGridInstance, nSteps, startingPoint,
                                                                           drift, diffusion, seed)
        return gbmPaths
    