import unittest

from NumericalSchemes.Utils import Utils


class TestUtils(unittest.TestCase):

    def test_init(self):
        x = Utils.initForProcesses(3, 10)
        self.assertTrue(len(x) == 10)
        self.assertTrue(len(x[0]) == 3)
