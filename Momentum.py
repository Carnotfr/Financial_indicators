#!/usr/bin/env python
# coding: utf-8

# # Momentum (MOM)

# Momentum is a technical indicator that measures the rate of change in an asset's price over a specified period. It shows the strength and direction of a price trend by comparing the current price of an asset to the price n periods ago.
# 
# The mathematical formula for momentum is:
# 
# Momentum = Current Price - Price n Periods Ago
# 
# where:
# 
# Current Price is the current market price of the asset.
# Price n Periods Ago is the market price of the asset n periods ago.
# The value of n can be set to any number of periods, but a common choice is 14 periods, which corresponds to two weeks of trading days.
# 
# For example, if the current price of an asset is $50 and the price 14 periods ago was $45, the momentum indicator value would be $5. If the current price is higher than the price n periods ago, the momentum indicator is positive, indicating a bullish trend. If the current price is lower than the price n periods ago, the momentum indicator is negative, indicating a bearish trend.

# In[ ]:


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# In[ ]:


nvidia_data = yf.download('NVDA', start='2022-04-20', end='2023-04-20')

close = nvidia_data['Close']

time_period = 20 # how far to look back to find reference price to compute momentum
history = [] # history of observed prices to use in momentum calculation
mom_values = [] # track momentum values for visualization purposes

for close_price in close:
  history.append(close_price)
  if len(history) > time_period: # history is at most 'time_period' number of observations
    del (history[0])

  mom = close_price - history[0]
  mom_values.append(mom)


# In[6]:


print(mom_values)


# In[4]:


print(close_price)


# In[12]:


nvidia_data = nvidia_data.assign(ClosePrice=pd.Series(close, index=nvidia_data.index))
nvidia_data = nvidia_data.assign(MomentumFromPrice20DaysAgo=pd.Series(mom_values, index=nvidia_data.index))

close_price = nvidia_data['ClosePrice']
mom = nvidia_data['MomentumFromPrice20DaysAgo']

fig = plt.figure()
ax1 = fig.add_subplot(211, ylabel='NVIDIA price in $')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
ax2 = fig.add_subplot(212, ylabel='Momentum in $')
mom.plot(ax=ax2, color='b', lw=2., legend=True)
plt.show()


# In[ ]:




