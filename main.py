import numpy as np
import matplotlib.pyplot as plt
from functions import brownian_motion


T=1 # Time horizon
N=1000 # Discretization number per time unit
delta_t = T/N
time = [_*delta_t for _ in range(N+1)]
BB = brownian_motion(T=T,N=N)

plt.plot(time,BB)
plt.show()