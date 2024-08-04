import unittest
import matplotlib.pyplot as plt
import numpy as np

import NumericalSchemes.RandomProcesses as RP
import NumericalSchemes.TimeGrid as TimeGrid


class RandomProcessesTest(unittest.TestCase):

    def test_generateBrownianMotion(self):
        np.random.seed(1)
        timeGridInstance = TimeGrid.TimeGrid(0, 1)
        random_movements = np.random.normal(size=10)
        print(random_movements)
        bb = RP.RandomProcesses.brownianMotionPath(timeGridInstance, 10, [0])
        plt.plot(bb)
        plt.show()


if __name__ == '__main__':
    unittest.main()
