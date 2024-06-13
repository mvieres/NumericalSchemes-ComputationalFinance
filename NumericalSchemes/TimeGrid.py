import numpy as np


class TimeGrid:

    def __init__(self, tStart: float, tEnd: float):
        self.tStart = tStart
        self.tEnd = tEnd
        self.alreadyComputed = {}  # integer n as key, value is boolean
        self.__timegrid = {}  # integer n as key, value is list of floats
        pass

    def computeTimeGrid(self, n: int) -> None:
        self.alreadyComputed[n] = True
        self.__timegrid = np.linspace(self.tStart, self.tEnd, n)

    def getTimeGrid(self, n: int) -> list:
        if not self.alreadyComputed[n]:  # TODO: Test this
            self.computeTimeGrid(n)
        return self.__timegrid[n]
