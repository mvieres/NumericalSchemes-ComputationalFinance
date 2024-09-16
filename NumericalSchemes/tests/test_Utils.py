import unittest

from NumericalSchemes.Utils import Utils


class TestUtils(unittest.TestCase):

    def test_init(self):
        x = Utils.initForProcesses([0, 0, 0], 10)
        self.assertTrue(len(x) == 10)
        self.assertTrue(len(x[0]) == 3)
