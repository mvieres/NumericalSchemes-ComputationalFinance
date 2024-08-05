import unittest

import matplotlib.pyplot as plt
import numpy as np

import NumericalSchemes.TimeGrid as TG


class TimeGridTest(unittest.TestCase):

    def test_computeTimeGrid(self):
        timeGridInstance = TG.TimeGrid(0, 1)
        tenor = timeGridInstance.getTimeGrid(3)
        areEqual = np.array_equal(tenor, [0, 0.5, 1])
        self.assertTrue(areEqual)
        timeGridInstance = TG.TimeGrid(0, 2)
        tenor = timeGridInstance.getTimeGrid(3)
        areEqual = np.array_equal(tenor, [0, 1, 2])
        self.assertTrue(areEqual)

    def testLD(self):
        date = TG.LocalDate(2020, 1, 1)
        date1 = TG.LocalDate(2021, 1, 1)
        date.setDiffToPreviousDate(date.date)
        self.assertEqual(date.getDiffToPreviousDate(), 0)
        date.setDiffToNextDate(date.date)
        self.assertEqual(date.getDiffToNextDate(), 0)


if __name__ == '__main__':
    unittest.main()
