
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

ticker = yf.Ticker('AAPL')
interest = yf.Ticker("^IRX")
expiration_date = '2024-09-27'

# Fetch the call options
calls = ticker.option_chain(expiration_date).calls
puts = ticker.option_chain(expiration_date).puts
int1 = 1

test = ticker.info['open']
print(test)
calls.to_csv('calls.csv')

# Plot Strike vs. Last Price for calls
plt.figure(figsize=(10, 6))
plt.plot(puts['strike'], puts['lastPrice'], marker='o')
plt.title('Apple Call Options: Strike Price vs. Last Price')
plt.xlabel('Strike Price')
plt.ylabel('Last Price')
plt.grid(True)
plt.show()