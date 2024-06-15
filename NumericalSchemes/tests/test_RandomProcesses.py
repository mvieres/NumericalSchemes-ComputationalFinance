import unittest
import matplotlib.pyplot as plt

import NumericalSchemes.RandomProcesses as RP
import NumericalSchemes.TimeGrid as TimeGrid


class RandomProcessesTest(unittest.TestCase):

    def test_generateBrownianMotion(self):
        timeGridInstance = TimeGrid.TimeGrid(0, 1)
        bb = RP.RandomProcesses.brownianMotionPath(timeGridInstance, 1000, [0])
        plt.plot(bb)
        plt.show()


if __name__ == '__main__':
    unittest.main()
