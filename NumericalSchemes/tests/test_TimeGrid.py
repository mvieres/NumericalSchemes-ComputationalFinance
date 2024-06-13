import unittest
import NumericalSchemes.TimeGrid as TG


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

    def test_computeTimeGrid(self):
        timeGridInstance = TG.TimeGrid(0, 1)
        tenor = timeGridInstance.getTimeGrid(3)
        self.assertEqual(tenor, [0, 0.5, 1])


if __name__ == '__main__':
    unittest.main()
