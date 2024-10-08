from Market.BlackScholes import BlackScholes
from Pricing.AmericanMonteCarlo.LongstaffSchwartzMonteCarlo import LongstaffSchwartzMonteCarlo as lsmc

import numpy as np
import time
import matplotlib.pyplot as plt


t_start = 0
t_end = 1
r = 0.06
sigma = 0.2
s0 = 36
strike = 33
bs_instance = BlackScholes(t_start=t_start, t_end=t_end, s0=s0, r=r, sigma=sigma)
payoff = lambda x: np.maximum(x - strike, 0)
degree = 5
#n_paths = [1000, 5000, 10000, 20000, 30000, 40000, 50000, 100000]
n_paths = [10**i for i in range(1, 7)]
#n_paths = [10, 20, 30, 40, 50]
n_steps = 100
res = np.zeros(shape=(len(n_paths), 5))

for N in n_paths:
    t_start = time.time()
    bs_instance.generate_scenarios(n_paths=N, n_steps=n_steps)
    lsm_instance = lsmc(bs_instance, payoff=payoff, n_paths=N, n_steps=n_steps)
    lsm_instance.set_degree(degree)
    lsm_instance.compute_option_price()
    end = time.time()
    res[n_paths.index(N), 0] = N
    res[n_paths.index(N), 1] = lsm_instance.value_0
    res[n_paths.index(N), 2] = lsm_instance.var_mc
    res[n_paths.index(N), 3] = lsm_instance.rmse
    res[n_paths.index(N), 4] = end - t_start

#plt.plot(np.log(res[:, 0]), np.log(res[:, 2]))
#plt.xlabel("log(N)")
#plt.ylabel("log(Variance)")
#plt.show()



plt.plot(np.log(res[:, 0]), np.log(res[:, 2]), 'x', color='black')
slope, intercept = np.polyfit(np.log(res[:, 0]), np.log(res[:, 2]), 1)
fitted_values = slope*np.log(res[:, 0]) + intercept
plt.plot(np.log(res[:, 0]), fitted_values, color='grey', linestyle='--')
plt.xticks(np.log(res[:, 0]), res[:, 0])
plt.xlabel('N')
plt.ylabel('log(var)')
plt.legend(['lsmc variance', 'Regression coefficient: ' + str(slope)])
plt.suptitle('Variance Reduction in N (log-log-plot)')
plt.title('Parameters: T=' + str(t_end) + ' K=' + str(strike) + ' n=' + str(n_steps) + ' m=' + str(degree) +
          ' r=' + str(r) + ' sigma='+ str(sigma) + ' s0=' + str(s0))
plt.savefig('convergence_N_variance_new_algo.png')
plt.show()