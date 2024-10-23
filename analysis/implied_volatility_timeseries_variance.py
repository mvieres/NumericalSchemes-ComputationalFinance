from Market.BlackScholes import BlackScholes
import numpy as np
import matplotlib.pyplot as plt

"""
The script showcases the difference between the parameter sigma in Black Scholes and the "variance" of the time series
"""

# Generate Black Scholes market data

sigma = 0.5
r = 0
s0 = 100
t_start = 0
t_end = 1
n_steps = 1000
n_samples = 6
scheme = "absolute_euler"
bs_instance = BlackScholes(t_start, t_end, s0, r, sigma, scheme)
bs_instance.generate_scenarios(n_samples, n_steps)
bs_instance.plot_underlying(legend=True)

# Lagged time series
time_series = bs_instance.scenarios
dt = bs_instance.time_grid_instance.get_time_grid(n_steps)[1] - bs_instance.time_grid_instance.get_time_grid(n_steps)[0]
returns = {}
relative_returns = {}
for key in time_series.keys():
    returns = np.log(time_series[key][1:] / time_series[key][:-1])
#plt.plot(bs_instance.time_grid_instance.get_time_grid(n_steps)[:-1], returns[0], label="Lagged time series")
#plt.show()
var_log_returns = np.var(returns)
sigma_estimated = np.sqrt(var_log_returns/dt)

"""
For Black scholes we have d S_t = r S_t dt + sigma S_t dW_t
Bluntly written, it is d S_t / S_t = r dt + sigma dW_t
Variance over the sample path is then 
"""



# Compare implied volatility with variance
for i in time_series.keys():
    print(f"Estimated volatility parameter sigma is: {sigma_estimated} and the parameter sigma is: {sigma}")