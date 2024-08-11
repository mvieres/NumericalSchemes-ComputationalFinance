import numpy as np


class Utils:

    @staticmethod
    def initForProcesses(startingPoint, nSteps):
        """
        Initialize random processes with this given structure.
        Change between one dimension and multidimensional cases.

        @param startingPoint:
        @param nSteps:
        @return:
        """
        if isinstance(startingPoint, (int, float)):
            x = np.zeros(nSteps)  # For single dimension
        else:
            x = np.zeros((nSteps, len(startingPoint)))  # For multi-dimension
        return x