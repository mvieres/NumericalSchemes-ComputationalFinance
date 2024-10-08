import unittest
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

import NumericalSchemes.RandomProcesses as RP
import NumericalSchemes.TimeGrid as TimeGrid


class RandomProcessesTest(unittest.TestCase):

    def test_generate_bm_non_equidistant(self):
        np.random.seed(1)
        timeGridInstance = TimeGrid.TimeGrid(0, 3)
        timeGridInstance.set_time_grid(3, [0, 1, 3])
        random_movements = np.random.normal(size=2)
        theoretical_value = np.array([0, np.sqrt(1)*random_movements[0], np.sqrt(1)*random_movements[0] + np.sqrt(2)*random_movements[1]])
        bb = RP.RandomProcesses.brownian_motion_path(timeGridInstance, 3, dimension=1, seed=1)
        self.assertTrue(np.array_equal(bb, theoretical_value))

    @unittest.skip("Plot for visual inspection")
    def test_generateMultipleBM(self):
        np.random.seed(100)
        time_grid_instance = TimeGrid.TimeGrid(0, 1)
        n_paths = 10
        bb = RP.RandomProcesses.multiple_brownian_motion_paths(time_grid_instance, n_paths, 1000, 1)
        for i in range(n_paths):
            plt.plot(time_grid_instance.get_time_grid(1000), bb[i])
        plt.show()

    def test_1d_brownian_motion_distribution(self):
        timeGridInstance = TimeGrid.TimeGrid(0, 1)
        n_steps = 1000
        bb = RP.RandomProcesses.multiple_brownian_motion_paths(timeGridInstance, 10000, n_steps, 1)
        end_values = np.array([bb[i][-1] for i in range(len(bb.keys()))])
        #plt.hist(end_values, bins=100)
        #plt.show()
        #stats.probplot(end_values, dist="norm", plot=plt)
        #plt.show()
        statistics, p_value = stats.kstest(end_values, 'norm', args=(0, np.sqrt(1)))
        # p_value > 0.05 means that H_0 (Normal(0,1) distribution) can not be rejected at the 5% level
        self.assertTrue(p_value > 0.05)

    @unittest.skip("Plot for visual inspection")
    def test_multidimesnisonal_brownian_motion(self):
        timeGridInstance = TimeGrid.TimeGrid(0, 10)
        n_steps = 1000
        bb = RP.RandomProcesses.brownian_motion_path(timeGridInstance, n_steps, 2)
        plt.plot(bb[:, 0], bb[:, 1])
        plt.show()

    @unittest.skip("Plot for visual inspection")
    def test_3d_brownian_motion(self):
        timeGridInstance = TimeGrid.TimeGrid(0, 10)
        n_steps = 1000
        bb = RP.RandomProcesses.brownian_motion_path(timeGridInstance, n_steps, 3)
        bb[:, 0], bb[:, 1] = np.meshgrid(bb[:, 0], bb[:, 1])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(bb[:, 0], bb[:, 1], bb[:, 2], cmap='viridis')
        plt.show()


if __name__ == '__main__':
    unittest.main()
