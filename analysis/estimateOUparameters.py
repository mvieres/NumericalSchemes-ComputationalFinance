# How to analyse ou parameters:
import numpy as np
import matplotlib.pyplot as plt

from NumericalSchemes.TimeGrid import TimeGrid
from NumericalSchemes.RandomProcesses import RandomProcesses

# 1. Create a time grid
timeGrid = TimeGrid(0, 1)
timeGrid.computeTimeGrid(1000)

theta = 1
mu = 0
sigma = 0.5

# 2. Create Ornstein-Uhlenbeck process paths
ouPaths = RandomProcesses.ornsteinUhlenbeckExactPaths(timeGrid, 100, 1000, 0, theta, mu, sigma)
# 3. OLS Regression of each time point
esitmatesTheta = np.zeros((1000, 1))

for i in range(0, 1000-1):
    x = np.array([ouPaths[j][i] for j in range(100)]).reshape(-1, 1)
    y = np.array([ouPaths[j][i+1] for j in range(100)]).reshape(-1, 1)
    esitmatesTheta[i] = np.linalg.lstsq(y, x, rcond=None)[0]

print("Estimated theta: " + str(np.mean(esitmatesTheta)))

plt.plot(esitmatesTheta)
plt.show()





