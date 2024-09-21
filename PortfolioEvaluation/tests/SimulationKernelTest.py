import unittest

from PortfolioEvaluation.SimulationKernel import SimulationKernel


class SimulationKernelTest(unittest.TestCase):

    def test_init(self):
        simulation_kernel = SimulationKernel()
        self.assertEqual(simulation_kernel.job_request, None)


if __name__ == '__main__':
    unittest.main()
