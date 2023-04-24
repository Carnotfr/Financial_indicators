#!/usr/bin/env python
# coding: utf-8

# # Standard Deviation

# Standard Deviation is a statistical calculation
#  used to measure the variability. In trading this value is known
#  as volatility. A low standard deviation indicates that the data
#  points tend to be very close to the mean, whereas high standard
#  deviation indicates that the data points are spread out over a large
#  range of values.
# 
# n = number of periods
# 
# Calculate the moving average.
#  The formula is:
# d = ((P1-MA)^2 + (P2-MA)^2 + ... (Pn-MA)^2)/n
# 
# Pn is the price you pay for the nth interval
# n is the number of periods you select
# 
# Take the square root of d. This gives you the standard deviation.
# 
# stddev = sqrt(d)

# In[3]:


import yfinance as yf
import pandas as pd
import statistics as stats
import matplotlib.pyplot as plt
import statistics as stats
import math as math


# In[4]:


start_date = '2022-04-24'
end_date = '2023-04-24'

goog = yf.Ticker("GOOG")
goog_data = goog.history(start=start_date, end=end_date)

close = goog_data['Close']
print(goog_data)


# In[5]:


time_period = 20 # look back period
history = [] # history of prices
sma_values = [] # to track moving average values for visualization purposes
stddev_values = [] # history of computed stdev values


# In[6]:


for close_price in close:
  history.append(close_price)
  if len(history) > time_period: # we track at most 'time_period' number of prices
    del (history[0])

  sma = stats.mean(history)
  sma_values.append(sma)
  variance = 0 # variance is square of standard deviation
  for hist_price in history:
    variance = variance + ((hist_price - sma) ** 2)

  stdev = math.sqrt(variance / len(history))

  stddev_values.append(stdev)


# In[9]:


print(history)


# In[15]:


goog_data = goog_data.assign(ClosePrice=pd.Series(close, index=goog_data.index))
goog_data = goog_data.assign(StandardDeviationOver20Days=pd.Series(stddev_values, index=goog_data.index))

close_price = goog_data['ClosePrice']
stddev = goog_data['StandardDeviationOver20Days']


# In[17]:


fig, ax1 = plt.subplots()
color = 'tab:green'
ax1.set_xlabel('Date')
ax1.set_ylabel('Google price in $', color=color)
close_price.plot(ax=ax1, color=color, lw=2., legend=True)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Stddev in $', color=color)
stddev.plot(ax=ax2, color=color, lw=2., legend=True)
ax2.axhline(y=stats.mean(stddev_values), color='k')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()


# In[ ]:




