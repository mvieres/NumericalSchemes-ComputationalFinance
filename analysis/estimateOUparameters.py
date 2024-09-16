# How to analyse ou parameters:
import numpy as np
import matplotlib.pyplot as plt

from NumericalSchemes.TimeGrid import TimeGrid
from NumericalSchemes.RandomProcesses import RandomProcesses
from NumericalSchemes.SdeSolver import SdeSolver

# 1. Create a time grid
timeGrid = TimeGrid(0, 1)

theta = 1
mu = 0
sigma = 1

# 2. Create Ornstein-Uhlenbeck process paths
dirft = lambda t, x: theta*(mu - x)
diffusion = lambda t, x: sigma

nPaths = 10
nSteps = 1000
ouPaths = {}
for numberPath in range(nPaths):
    ouPaths[numberPath] = SdeSolver.euler(timeGrid, nSteps, 0, dirft, diffusion)
# 3. OLS Regression of each time point
esitmatesTheta = np.zeros((nSteps-3, 1))

for i in range(1, nSteps-2):
    x = np.array([ouPaths[j][i] for j in range(nPaths)]).reshape(-1, 1)
    y = np.array([ouPaths[j][i+1] for j in range(nPaths)]).reshape(-1, 1)
    esitmatesTheta[i-1] = np.linalg.lstsq(y, x, rcond=None)[0]

print("Estimated theta: " + str(np.mean(esitmatesTheta)))


plt.plot(esitmatesTheta)
plt.show()