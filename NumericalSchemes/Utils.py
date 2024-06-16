import numpy as np


class Utils:

    @staticmethod
    def initForProcesses(startingPoint, nSteps):
        if isinstance(startingPoint, (int, float)):
            x = np.zeros(nSteps)  # For single dimension
        else:
            x = np.zeros((nSteps, len(startingPoint)))  # For multi-dimension
        return x