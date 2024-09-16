import numpy as np

from NumericalSchemes.TimeGrid import TimeGrid
from NumericalSchemes.TimeGrid import Calendar
from Market.TrolleSchwartz import TrolleSchwartz


class YieldCurveContainer:

    """
    Compute and store the yield curve for a given time grid / calendar.
    The idea is to offer possibilities to pre-compute the yield curve for the given grid.
    Nevertheless, there is also the possibility to compute the yield curve during pricing simulation.
    TODO: needs new spezification
    """
    def __init__(self, calendar_or_timegrid: Calendar or TimeGrid = None):
        if calendar is not None and timegrid is None:
            assert isinstance(calendar, Calendar), "Calendar must be of type Calendar"
            self.calendar = calendar
            self.timegrid = calendar.get_time_grid()
            return
        if timegrid is not None and calendar is None:
            assert isinstance(timegrid, TimeGrid), "Timegrid must be of type TimeGrid"
            self.timegrid = timegrid
            return
        raise ValueError("Either calendar or timegrid must be given")

    def setCalender(self, calendar: Calendar):
        self.calendar = calendar

    def setTimeGrid(self, timegrid: TimeGrid):
        self.timegrid = timegrid

    def computeYieldCurveForCalendar(self):
        """
        Compute the yield curve for every dt in the calendar. Keep in mind that dt = 1 equals a difference of one day.
        This method computes the overall yield curve for the complete time span and for each unique dt.
        :param timeGrid: TimeGrid, time grid instance
        """
        assert self.calendar is not None, "Calendar must be set"
        # TODO: Blocked by meaningful implementation for calendar
        pass

    def computeYieldCurveForTimeGrid(self):
        """
        Compute the yield curve for every dt in the time grid. This method computes the overall yield curve for the
        complete time span and for each unique dt.
        :param timeGrid: TimeGrid, time grid instance
        """
        assert self.timegrid is not None, "Timegrid must be set"
        # TODO: Check that Timegrid has meaningful values
        unique_differences = self.compute_unique_differences(self.timegrid.get_time_grid())

        self.yield_curve = {} # dict of dicts: first comes the number of points in the grid (n) and then the yield curve
        time_grid_keys = self.timegrid.get_time_grid().keys()
        for n in time_grid_keys:
            self.yield_curve[n] = {}
            for dt in unique_differences:
                self.yield_curve[n][dt] = self.compute_yield_curve_for_dt(dt)

    def compute_yield_curve_for_dt(self, dt):
        """
        Compute the yield curve for the given dt, use the TrolleSchwartz model for that.
        :param dt: float, time difference
        :return: list[float], yield curve for the given dt
        """
        # TODO: figure out where to setup these parameters
        alpha_0 = 1
        alpha_1 = 1
        gamma = 1
        kappa = 1
        theta = 1
        sigma = 1

        return 0.1

    def getYieldCurve(self, lendingTime: float):
        """Returns the complete yield curve for the given lending time."""
        return 1.1

    def getShortRate(self, lendingTime: float):
        """Returns the short rate (interest rate at t=0) for the given lending time."""
        return self.getYieldCurve(lendingTime) - 1

    @staticmethod
    def compute_unique_differences(points):
        unique_differences = set()
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                difference = abs(points[i] - points[j])
                unique_differences.add(difference)
        return list(unique_differences)
