import numpy as np


class TimeGrid:

    def __init__(self, tStart: float, tEnd: float):
        self.tStart = tStart
        self.tEnd = tEnd
        self.__timegrid = {}  # integer as key, value is numpy array of time grid points

    def computeTimeGrid(self, n: int) -> None:
        self.__timegrid[n] = np.linspace(self.tStart, self.tEnd, n)

    def getTimeGrid(self, n: int) -> np.array:
        if not self.__checkIfKeyAlreadyExists(n):
            self.computeTimeGrid(n)
        return self.__timegrid[n]

    def setTimeGrid(self, n: int, points: list[float]):
        assert not self.__checkIfKeyAlreadyExists(n), "Time grid already exists w.r.t. n points!"
        assert len(points) == n, "Number of points has to be equal to n"
        assert max(list) < self.tEnd, "Time points have to be in the interval [tStart, tEnd]"
        assert min(list) > self.tStart, "Time points have to be in the interval [tStart, tEnd]"
        self.__timegrid[n] = np.array(points)

    def getDtDiffToPreviousPoint(self, n: int, i: int) -> float:
        assert i > 0, "i has to be bigger than 0"
        return self.__timegrid[n][i] - self.__timegrid[n][i - 1]

    def getDtDiffToNextPoint(self, n: int, i: int) -> float:
        assert i > 0, "i has to be bigger than 0"
        return self.__timegrid[n][i] - self.__timegrid[n][i - 1]

    def __checkIfKeyAlreadyExists(self, n: int) -> bool:
        return n in self.__timegrid.keys()
