
import yfinance as yf
import matplotlib.pyplot as plt


ticker = yf.Ticker('AAPL')
expiration_date = '2024-09-27'

# Fetch the call options
calls = ticker.option_chain(expiration_date).calls
puts = ticker.option_chain(expiration_date).puts
int1 = 1
calls.to_csv('calls.csv')

# Plot Strike vs. Last Price for calls
plt.figure(figsize=(10, 6))
plt.plot(puts['strike'], puts['lastPrice'], marker='o')
plt.title('Apple Call Options: Strike Price vs. Last Price')
plt.xlabel('Strike Price')
plt.ylabel('Last Price')
plt.grid(True)
plt.show()