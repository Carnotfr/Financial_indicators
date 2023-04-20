#!/usr/bin/env python
# coding: utf-8

# # MACD

# MACD (Moving Average Convergence Divergence) is a popular technical indicator that helps traders and investors identify potential trend reversals and momentum shifts in the market. The MACD is calculated by subtracting a longer-term exponential moving average (EMA) from a shorter-term EMA. The result is a single line that oscillates above and below a center or zero line. The MACD can also be used with a signal line, which is typically a 9-day EMA of the MACD itself.
# 
# When the MACD line crosses above the signal line, it is considered a bullish signal, suggesting that the stock price may be trending upward. Conversely, when the MACD line crosses below the signal line, it is considered a bearish signal, indicating that the stock price may be trending downward.
# MACD Line = 12-day EMA - 26-day EMA
# Signal Line = 9-day EMA of MACD Line
# 
# The MACD histogram is calculated by taking the difference between the MACD line and the signal line. It oscillates above and below a center or zero line, and can help traders and investors identify changes in momentum.
# 
# It's worth noting that while the MACD is a popular technical indicator, it should not be relied on solely for making investment decisions. Traders and investors should use multiple indicators and analysis techniques to make informed decisions about when to buy, hold, or sell a particular stock or security.

# In[20]:


import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[21]:


# Download the data for NVIDIA from the last year up to now
nvda = yf.download('NVDA', period='1y')

# Define the parameters for the MACD indicator
fast_ema = 12
slow_ema = 26
signal_ema = 9


# In[22]:


# Calculate the fast and slow EMA
ema_fast = nvda['Adj Close'].ewm(span=fast_ema, adjust=False).mean()
ema_slow = nvda['Adj Close'].ewm(span=slow_ema, adjust=False).mean()


# In[23]:


# Calculate the MACD line and signal line
macd_line = ema_fast - ema_slow
signal_line = macd_line.ewm(span=signal_ema, adjust=False).mean()

# Calculate the MACD histogram
macd_histogram = macd_line - signal_line


# In[24]:


# Add the MACD values to the DataFrame
nvda['MACD'] = macd_line
nvda['Signal Line'] = signal_line
nvda['MACD Histogram'] = macd_histogram


# In[25]:


# Plot the closing price and MACD values
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12,8))

ax1.set_ylabel('Closing Price ($)')
ax1.plot(nvda.index, nvda['Adj Close'])
ax1.set_title('NVIDIA Stock Price')

ax2.set_ylabel('MACD')
ax2.plot(nvda.index, nvda['MACD'], label='MACD')
ax2.plot(nvda.index, nvda['Signal Line'], label='Signal Line')
ax2.bar(nvda.index, nvda['MACD Histogram'], label='MACD Histogram', color='grey')
ax2.legend()
ax2.set_title('MACD Indicator')

plt.show()


# In[ ]:




