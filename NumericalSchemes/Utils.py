import numpy as np


class Utils:

    @staticmethod
    def initForProcesses(dimension, nSteps):
        """
        Initialize random processes with this given structure.
        Change between one dimension and multidimensional cases.

        @param startingPoint:
        @param nSteps:
        @return:
        """
        if dimension == 1:
            x = np.zeros(nSteps)  # For single dimension
        else:
            x = np.zeros((nSteps, dimension))  # For multi-dimension
        return x