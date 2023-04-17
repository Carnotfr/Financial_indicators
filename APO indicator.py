#!/usr/bin/env python
# coding: utf-8

# # A Python Script for Stock Price Analysis of TSM with APO Indicator

# This script uses Python libraries like pandas and yfinance to download historical stock data for a company called TSM from Yahoo Finance. The data is saved in a file called "tsm_data.pkl" to avoid redownloading it if it already exists.
# 
# After downloading the data, the script calculates the Absolute Price Oscillator (APO), which is a technical indicator used to determine the momentum of a stock's price trend. It does this by calculating the difference between two exponential moving averages (EMAs) of different lengths, a "Fast" and a "Slow" EMA.
# 
# The script then calculates the Fast EMA and Slow EMA for TSM's stock price using the downloaded data, and uses those values to calculate the APO. It then adds these calculated values to the data that was downloaded earlier, and finally creates a graph using the matplotlib library to visualize the TSM stock price, the Fast EMA, the Slow EMA, and the APO.
# 
# Overall, this script demonstrates how to use Python to download and analyze historical stock data and use it to calculate technical indicators to gain insights into the stock's price trend.

# In[2]:


import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# In[3]:


start_date = "2019-01-01"
end_date = "2023-04-13"
DATA_SRC_FILENAME = 'tsm_data.pkl'


# In[4]:


try:
    tsm_data2 = pd.read_pickle(DATA_SRC_FILENAME)
except FileNotFoundError:
    tsm_data2 = yf.download('TSM', start_date, end_date)
    tsm_data2.to_pickle(DATA_SRC_FILENAME)


# In[5]:


print(tsm_data2)


# In[6]:


tsm_data = tsm_data2.tail(620)


# In[7]:


print(tsm_data)


# In[8]:


close = tsm_data['Close']


# APO = Fast Exponential Moving Average - Slow Exponential Moving Average

# In[9]:


num_periods_fast = 20 # time period for the fast EMA
num_periods_slow = 50 # time period for slow EMA


# In[10]:


K_fast = 2 / (num_periods_fast + 1) # smoothing factor for fast EMA
K_slow = 2 / (num_periods_slow + 1) # smoothing factor for slow EMA


# The smoothing factor, also known as the weighting factor, determines the degree of weighting decrease applied to each past price in the moving average calculation. The larger the value of the smoothing factor, the more weight is given to the most recent price data, resulting in a faster response to the price changes. In contrast, a smaller smoothing factor gives more weight to the historical price data, resulting in a slower response to the price changes.
# 
# The values of K_fast and K_slow in the code are calculated using the formula for exponential smoothing, which is a popular method for calculating the moving average. The formula uses the number of periods in the moving average to calculate the smoothing factor. A common value for the number of periods in a moving average is 20 for fast EMA and 50 for slow EMA. The smoothing factor is calculated as 2 divided by the number of periods plus 1. The resulting value is then used in the exponential smoothing formula to calculate the EMA for each period.

# In[28]:


# calculate Exponential Moving Averages and Absolute Price Oscillator
close = tsm_data['Close']
ema_fast_values = []
ema_slow_values = []
apo_values = []
K_fast = 2 / (10 + 1)
K_slow = 2 / (40 + 1)
ema_fast = 0
ema_slow = 0


# In[29]:


for close_price in close:
    if ema_fast == 0:  # first observation
        ema_fast = close_price
        ema_slow = close_price
    else:
        ema_fast = (close_price - ema_fast) * K_fast + ema_fast
        ema_slow = (close_price - ema_slow) * K_slow + ema_slow
    ema_fast_values.append(ema_fast)
    ema_slow_values.append(ema_slow)
    apo_values.append(ema_fast - ema_slow)


# ema_fast = (Close - EMA(previous)) x K_fast + EMA(previous)
# 
# ema_slow = (Close - EMA(previous)) x K_slow + EMA(previous)
# 

# In[30]:


# create new columns for the calculated values
tsm_data = tsm_data.assign(ClosePrice=close)
tsm_data = tsm_data.assign(FastExponential10DayMovingAverage=ema_fast_values)
tsm_data = tsm_data.assign(SlowExponential40DayMovingAverage=ema_slow_values)
tsm_data = tsm_data.assign(AbsolutePriceOscillator=apo_values)


# In[31]:


#Assigning variables to the newly created columns
close_price = tsm_data['ClosePrice']
ema_f = tsm_data['FastExponential10DayMovingAverage']
ema_s = tsm_data['SlowExponential40DayMovingAverage']
apo = tsm_data['AbsolutePriceOscillator']


# In[39]:


fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel='TSM price in $')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ema_f.plot(ax=ax1, color='b', lw=2., legend=True)
ema_s.plot(ax=ax1, color='r', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='APO')
apo.plot(ax=ax2, color='black', lw=2., legend=True)
plt.show()


# In[ ]:




