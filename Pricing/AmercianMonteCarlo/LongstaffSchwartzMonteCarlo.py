import numpy as np

from Market.BlackScholes import BlackScholes
from Market.YieldCurveContainer import YieldCurveContainer


class LongstaffSchwartzMonteCarlo:

    def __init__(self, underlyingInstance: BlackScholes, payoff: callable, nPaths: int, nSteps: int):
        self.underlyingInstance = underlyingInstance
        self.nPaths = nPaths
        self.nSteps = nSteps
        self.payoff = payoff
        self.timeGridInstance = self.underlyingInstance.timeGridInstance  # TODO: check that this is a pointer
        self.regressiontype = "polynomial"
        self.calender = underlyingInstance.timeGridInstance.get_time_grid(self.nSteps)
        self.regression_types ={
            "legendre": np.polynomial.legendre.legfit,
            "laguerre": np.polynomial.laguerre.lagfit,
            "polynomial": np.polyfit
        }
        self.yield_curve_instance = YieldCurveContainer(self.timeGridInstance.get_time_grid(self.nSteps))
        pass

    def reset(self):
        self.__init__(self.underlyingInstance, self.payoff, self.nPaths, self.nSteps)

    def setRegressionType(self, regressiontype: str):
        self.regressiontype = regressiontype

    def generateNewSamples(self):
        self.underlyingInstance.computeSolutionPath(self.nSteps)

    def computeOptionPrice(self) -> float:


        pass