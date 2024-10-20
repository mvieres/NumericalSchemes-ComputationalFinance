from Market.BlackScholes import BlackScholes
import numpy as np
import matplotlib.pyplot as plt

"""
The script showcases the difference between the parameter sigma in Black Scholes and the "variance" of the time series
"""

# Generate Black Scholes market data

sigma = 0.5
r = 0.1
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
returns = {}
relative_returns = {}
for key in time_series.keys():
    returns[key] = time_series[key][1:] - time_series[key][:-1]
    relative_returns = returns[key] / time_series[key][:-1] # This is not right
plt.plot(bs_instance.time_grid_instance.get_time_grid(n_steps)[:-1], returns[0], label="Lagged time series")
plt.show()


"""
For Black scholes we have d S_t = r S_t dt + sigma S_t dW_t
Bluntly written, it is d S_t / S_t = r dt + sigma dW_t
Variance over the sample path is then 
"""



# Compare implied volatility with variance
for i in time_series.keys():
    print(f"Variance of original time series is: {np.var(time_series[i])}, variance of lagged series is {np.var(returns[i])}, variance of relative returns is {np.var(relative_returns[i])}")