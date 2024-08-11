import numpy as np

#from Market.Heston import Heston
from Market.BlackScholes import BlackScholes


class LongstaffSchwartzMonteCarlo:

    def __init__(self, underlyingInstance: BlackScholes, payoff: callable, nPaths: int, nSteps: int):
        self.underlyingInstance = underlyingInstance
        self.nPaths = nPaths
        self.nSteps = nSteps
        self.g = payoff
        self.timeGridInstance = self.underlyingInstance.timeGridInstance  # TODO: check that this is a pointer
        self.regressiontype = "polynomial"
        self.calender = underlyingInstance.timeGridInstance.getTimeGrid(self.nSteps)
        pass

    def setRegressionType(self, regressiontype: str):
        self.regressiontype = regressiontype

    def generateNewSamples(self):
        self.underlyingInstance.computeSolutionPath(self.nSteps)

    def computeOptionPrice(self) -> float:


        pass