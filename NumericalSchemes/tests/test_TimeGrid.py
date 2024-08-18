import unittest

import matplotlib.pyplot as plt
import numpy as np

import NumericalSchemes.TimeGrid as TG


class TimeGridTest(unittest.TestCase):

    def test_computeTimeGrid(self):
        timeGridInstance = TG.TimeGrid(0, 1)
        tenor = timeGridInstance.get_time_grid(3)
        areEqual = np.array_equal(tenor, [0, 0.5, 1])
        self.assertTrue(areEqual)
        timeGridInstance = TG.TimeGrid(0, 2)
        tenor = timeGridInstance.get_time_grid(3)
        areEqual = np.array_equal(tenor, [0, 1, 2])
        self.assertTrue(areEqual)

    def test_get_differences_equidistant(self):
        timeGridInstance = TG.TimeGrid(0, 1)
        self.assertEqual(timeGridInstance.get_dt_diff_to_previous_point(3, 1), 0.5)
        self.assertEqual(timeGridInstance.get_dt_diff_to_previous_point(3, 2), 0.5)
        self.assertEqual(timeGridInstance.get_dt_diff_to_next_point(3, 0), 0.5)

    def test_get_differences_non_equidistant(self):
        time_grid_instance = TG.TimeGrid(0, 10)
        time_grid_instance.set_time_grid(3, [0, 3, 10])
        self.assertEqual(time_grid_instance.get_dt_diff_to_previous_point(3, 1), 3)
        self.assertEqual(time_grid_instance.get_dt_diff_to_previous_point(3, 2), 7)
        self.assertEqual(time_grid_instance.get_dt_diff_to_next_point(3, 0), 3)
        self.assertEqual(time_grid_instance.get_dt_diff_to_next_point(3, 1), 7)

    def testLD(self):
        date = TG.LocalDate(2020, 1, 1)
        date1 = TG.LocalDate(2021, 1, 1)
        date.set_diff_to_previous_date(date.date)
        self.assertEqual(date.get_diff_to_previous_date(), 0)
        date.set_diff_to_next_date(date.date)
        self.assertEqual(date.get_diff_to_next_date(), 0)


if __name__ == '__main__':
    unittest.main()
