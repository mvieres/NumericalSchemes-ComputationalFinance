import numpy as np
import datetime
import pandas as pd

# TODO: This file needs work, i.e. TimeGrid is used for simple calculations on a gird. Everything else needs to be specified

class LocalDate:
    def __init__(self, year: int, month: int, day: int):
        self.date = datetime.date(year, month, day)
        self.diffToPreviousDate = None
        self.diffToNextDate: float

    def getDiffToPreviousDate(self) -> float:
        return self.diffToPreviousDate

    def getDiffToNextDate(self) -> float:
        return self.diffToNextDate

    def setDiffToPreviousDate(self, previousDate: datetime.date) -> None:
        self.diffToPreviousDate = (self.date - previousDate).days

    def setDiffToNextDate(self, nextDate: datetime.date) -> None:
        self.diffToNextDate = (nextDate - self.date).days

    def asOrdinal(self):
        return self.date.toordinal()  # This is used to get diff w.r.t. days


class TimeGrid:

    def __init__(self, tStart: float or datetime, tEnd: float or datetime):
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
        assert i < len(self.__timegrid[n])-1, "i has to be at most the first to last index"
        return self.__timegrid[n][i + 1] - self.__timegrid[n][i]

    def __checkIfKeyAlreadyExists(self, n: int) -> bool:
        return n in self.__timegrid.keys()


class Calendar(TimeGrid):
    """
    This class is a colection of local dates. This forms a calendar. The calendar is used to hold all relevant
    simulation dates for the monte carlo simulation. If the total number of simulation dates is rather low, the gird is
    enriched with a given number of points between. The default timescale is given in days. Hence, this class cannot be
    used to simulate intraday trading.
    """
    def __init__(self, simulationDates: list[LocalDate]):
        tStart = min(simulationDates, key=lambda date: date.date)
        tEnd = max(simulationDates, key=lambda date: date.date)
        super().__init__(tStart, tEnd)
        self.__dates = {}
        self.__simulationDates = simulationDates
        self.simulationCalender = None

    def setTimeGrid(self, n: int):
        pass

    def is_business_day(date):
        return pd.bdate_range(start=date, end=date).size > 0