import numpy as np


class TimeGrid:

    def __init__(self, tStart: float, tEnd: float):
        self.tStart = tStart
        self.tEnd = tEnd
        self.__timegrid = {}  # integer as key, value is numpy array of time grid points
        pass

    def computeTimeGrid(self, n: int) -> None:
        self.__timegrid[n] = np.linspace(self.tStart, self.tEnd, n)

    def getTimeGrid(self, n: int) -> np.array:
        if not self.__checkIfKeyAlreadyExists(n):
            self.computeTimeGrid(n)
        return self.__timegrid[n]

    def __checkIfKeyAlreadyExists(self, n: int) -> bool:
        return n in self.__timegrid.keys()
