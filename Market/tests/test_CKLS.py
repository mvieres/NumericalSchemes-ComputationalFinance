import unittest

from Market.CKLS import CKLS


class CKLSTest(unittest.TestCase):

    def test_functionality_aboslute_euler(self):
        t_start = 0
        t_end = 1
        x0 = 1
        theta = 1
        kappa = 0.1
        sigma = 0.5
        gamma = 0.7
        scheme = "absolute_euler"
        ckls_instance = CKLS(t_start, t_end, x0, theta, kappa, sigma, gamma, scheme)
        try:
            ckls_instance.generate_scenarios(4, 10)
        except Exception as e:
            self.fail(f"Failed with exception {e}")

if __name__ == '__main__':
    unittest.main()
