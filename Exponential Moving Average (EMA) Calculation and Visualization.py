#!/usr/bin/env python
# coding: utf-8

# # Exponential Moving Average (EMA) Calculation and Visualization

# Description: This code calculates and visualizes the Exponential Moving Average (EMA) for a given stock using the finance library. The EMA is a technical indicator that places more weight on recent prices and is useful for identifying trends and potential price reversals. The code reads in stock price data for a given period, calculates the EMA over a specified number of periods, and then plots the EMA and closing price on a graph for visual analysis.

# In[ ]:


import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


# Define the start and end dates
start_date = '2022-04-17'
end_date = '2023-04-17'

# Fetch the data using yfinance
nvda_data = yf.download('NVDA', start=start_date, end=end_date)

# Extract the closing price
close = nvda_data['Close']


# In[ ]:


# Calculate the Exponential Moving Average (EMA)
num_periods = 20 # number of days over which to average
K = 2 / (num_periods + 1) # smoothing constant
ema_p = 0
ema_values = [] # to hold computed EMA values
for close_price in close:
    if (ema_p == 0): # first observation, EMA = current-price
        ema_p = close_price
    else:
        ema_p = (close_price - ema_p) * K + ema_p
    ema_values.append(ema_p)


# The EMA is calculated using the following formula:
# 
# EMA = (P - EMAp) * K + EMAp
# 
# Where:
# 
# P = Price for the current period
# EMAp = the Exponential Moving Average for the previous period
# K = the smoothing constant, which is calculated as 2 / (n + 1) where n is the number of periods used for the EMA
# n = the number of periods in a simple moving average, which is roughly approximated by the EMA

# In[3]:


# Add the closing price and EMA to the dataframe
nvda_data = nvda_data.assign(ClosePrice=pd.Series(close, index=nvda_data.index))
nvda_data = nvda_data.assign(Exponential20DayMovingAverage=pd.Series(ema_values, index=nvda_data.index))

# Plot the data
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='NVIDIA price in $')
close.plot(ax=ax1, color='g', lw=2., legend=True)
nvda_data['Exponential20DayMovingAverage'].plot(ax=ax1, color='b', lw=2., legend=True)
plt.show()

