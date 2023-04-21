#!/usr/bin/env python
# coding: utf-8

# # Relative Strength Index(RSI)

# RSI stands for Relative Strength Index, which is a technical analysis indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in an asset.
# 
# The RSI is calculated using the following formula:
# 
# RSI = 100 - (100 / (1 + RS))
# 
# Where:
# RS = the ratio of the smoothed average of n-period gains divided by the absolute value of the smoothed average of n-period losses.
# 
# The typical time period used for RSI calculation is 14, but it can be adjusted to suit different trading styles and market conditions.
# 
# When the RSI value is above 70, it is generally considered overbought and may indicate a potential price reversal to the downside. Conversely, when the RSI value is below 30, it is generally considered oversold and may indicate a potential price reversal to the upside. However, traders should use the RSI in conjunction with other technical indicators and market analysis tools to make informed trading decisions.

# In[12]:


import yfinance as yf
import pandas as pd
import statistics as stats
import matplotlib.pyplot as plt


# In[13]:


start_date = '2022-04-20'
end_date = '2023-04-20'

nvidia = yf.Ticker("NVDA")
nvidia_data = nvidia.history(start=start_date, end=end_date)

close = nvidia_data['Close']
print(nvidia_data)


# In[14]:


time_period = 20 # look back period to compute gains & losses
gain_history = [] # history of gains over look back period (0 if no gain, magnitude of gain if gain)
loss_history = [] # history of losses over look back period (0 if no loss, magnitude of loss if loss)
avg_gain_values = [] # track avg gains for visualization purposes
avg_loss_values = [] # track avg losses for visualization purposes
rsi_values = [] # track computed RSI values
last_price = 0 # current_price - last_price > 0 => gain. current_price - last_price < 0 => loss.


# In[15]:


for close_price in close:
    if last_price == 0:
        last_price = close_price

    gain_history.append(max(0, close_price - last_price))
    loss_history.append(max(0, last_price - close_price))
    last_price = close_price

    if len(gain_history) > time_period: # maximum observations is equal to lookback period
        del (gain_history[0])
        del (loss_history[0])

    avg_gain = stats.mean(gain_history) # average gain over lookback period
    avg_loss = stats.mean(loss_history) # average loss over lookback period

    avg_gain_values.append(avg_gain)
    avg_loss_values.append(avg_loss)

    rs = 0
    if avg_loss > 0: # to avoid division by 0, which is undefined
        rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))
    rsi_values.append(rsi)


# In[16]:


print(last_price)


# In[17]:


print(avg_gain)


# In[18]:


print(close_price)


# In[19]:


print(avg_gain_values)


# In[20]:


print(avg_loss)


# In[21]:


print(rs)


# In[23]:


nvidia_data = nvidia_data.assign(ClosePrice=close.values)
nvidia_data = nvidia_data.assign(RelativeStrengthAvgGainOver20Days=avg_gain_values)
nvidia_data = nvidia_data.assign(RelativeStrengthAvgLossOver20Days=avg_loss_values)
nvidia_data = nvidia_data.assign(RelativeStrengthIndicatorOver20Days=rsi_values)

close_price = nvidia_data['ClosePrice']
rs_gain = nvidia_data['RelativeStrengthAvgGainOver20Days']
rs_loss = nvidia_data['RelativeStrengthAvgLossOver20Days']
rsi = nvidia_data['RelativeStrengthIndicatorOver20Days']

fig, axs = plt.subplots(3, 1, figsize=(12, 10))

axs[0].plot(close_price, color='black', lw=2., label='NVIDIA Price')
axs[0].legend(loc='upper left')

axs[1].plot(rs_gain, color='g', lw=2., label='RSI Avg Gain')
axs[1].plot(rs_loss, color='r', lw=2., label='RSI Avg Loss')
axs[1].legend(loc='upper left')

axs[2].plot(rsi, color='b', lw=2., label='RSI')
axs[2].legend(loc='upper left')

plt.show()


# In[ ]:





# In[ ]:




