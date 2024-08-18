import numpy as np
import datetime
import pandas as pd

# TODO: This file needs work, i.e. TimeGrid is used for simple calculations on a gird. Everything else needs to be specified


class LocalDate:
    def __init__(self, year: int, month: int, day: int):
        self.date = datetime.date(year, month, day)
        self.diffToPreviousDate = None
        self.diffToNextDate: float

    def get_diff_to_previous_date(self) -> float:
        return self.diffToPreviousDate

    def get_diff_to_next_date(self) -> float:
        return self.diffToNextDate

    def set_diff_to_previous_date(self, previousDate: datetime.date) -> None:
        self.diffToPreviousDate = (self.date - previousDate).days

    def set_diff_to_next_date(self, nextDate: datetime.date) -> None:
        self.diffToNextDate = (nextDate - self.date).days

    def as_ordinal(self):
        return self.date.toordinal()  # This is used to get diff w.r.t. days


class TimeGrid:
    """
    TimeGrid creates an equidistant time grid. It stores different grids with respect to the number of points n.
    """

    def __init__(self, t_start: float or datetime, t_end: float or datetime):
        self.tStart = t_start
        self.tEnd = t_end
        self.__timegrid = {}  # integer as key, value is numpy array of time grid points

    def compute_time_grid(self, n: int) -> None:
        self.__timegrid[n] = np.linspace(self.tStart, self.tEnd, n)

    def get_time_grid(self, n=None) -> np.array:
        """
        Returns the time grid with respect to the number of points n. If n is None, the complete dict of time-grids
        is returned.
        """
        if n is not None:
            assert isinstance(n, int), "n has to be an integer"
        if not self.__checkIfKeyAlreadyExists(n):
            self.compute_time_grid(n)
        if n is None:
            return self.__timegrid
        else:
            return self.__timegrid[n]

    def set_time_grid(self, n: int, points: list[float]):
        assert not self.__checkIfKeyAlreadyExists(n), "Time grid already exists w.r.t. n points!"
        assert len(points) == n, "Number of points has to be equal to n"
        assert max(points) <= self.tEnd, "Time points have to be in the interval [tStart, tEnd]"
        assert min(points) >= self.tStart, "Time points have to be in the interval [tStart, tEnd]"
        self.__timegrid[n] = np.array(points)

    def get_dt_diff_to_previous_point(self, n: int, i: int) -> float:
        assert i > 0, "i has to be bigger than 0"
        if n not in self.__timegrid.keys():
            self.initialize_time_grid_fallback(n)
        return self.__timegrid[n][i] - self.__timegrid[n][i - 1]

    def get_dt_diff_to_next_point(self, n: int, i: int) -> float:
        assert i < len(self.__timegrid[n])-1, "i has to be at most the first to last index"
        if n not in self.__timegrid.keys():
            self.initialize_time_grid_fallback(n)
        return self.__timegrid[n][i + 1] - self.__timegrid[n][i]

    def initialize_time_grid_fallback(self, n: int) -> None:
        """
        Compute time grid if not initialized yet. Default is the equidistant time grid.
        """
        self.compute_time_grid(n)

    def __checkIfKeyAlreadyExists(self, n: int) -> bool:
        return n in self.__timegrid.keys()


class Calendar(TimeGrid):
    """
    Calendar is a collection of local dates. This dates from a rather simple time grid. To use this grid for computing,
    calendar entries are translated to a simple time grid that operates on floats. The reference time scale is "days",
    i.e. the difference between two consecutive business days within a week is 1, if there is a weekend in between, it
    is 3.
    TODO: Not final, needs better specification
    """

    def __init__(self, simulationDates: list[LocalDate]):
        tStart = min(simulationDates, key=lambda date: date.date)
        tEnd = max(simulationDates, key=lambda date: date.date)
        super().__init__(tStart, tEnd)
        self.__dates = {}
        self.__simulationDates = simulationDates
        self.simulationCalender = None

    def set_time_grid(self, n: int):
        pass

    def is_business_day(date):
        return pd.bdate_range(start=date, end=date).size > 0