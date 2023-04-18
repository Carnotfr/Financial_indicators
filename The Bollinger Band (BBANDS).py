#!/usr/bin/env python
# coding: utf-8

# # The Bollinger Band (BBANDS) 

# The Bollinger Band is a popular technical analysis tool that is used to measure volatility in financial markets. It consists of a middle band that is a simple moving average of prices and an upper and lower band that are a certain number of standard deviations away from the middle band. In this code, the Bollinger Band is calculated for Nvidia's stock price over the past year and used to visualize the upper and lower price ranges around the stock's moving average. This allows traders and investors to identify potential buy or sell signals based on whether the price is approaching or crossing the upper or lower bands, respectively.

# In[20]:


import yfinance as yf
import statistics as stats
import math as math
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[21]:


nvidia = yf.Ticker("NVDA")
start_date = '2022-04-17'
end_date = '2023-04-17'
nvda_data = nvidia.history(start=start_date, end=end_date)
close = nvda_data['Close']
print(nvda_data)


# In[29]:


time_period = 20 # history length for Simple Moving Average for middle band
stdev_factor = 2 # Standard Deviation Scaling factor for the upper and lower bands
history = [] # price history for computing simple moving average
sma_values = [] # moving average of prices for visualization purposes
upper_band = [] # upper band values
lower_bound = [] # lower band values


# The Bollinger Band (BBANDS) study created by John Bollinger plots upper and lower envelope bands around the price of the instrument. The width of the bands is based on the standard deviation of the closing prices from a moving average of price.
#  Middle Band = n-period moving average
# 
# Upper Band = Middle Band + ( y * n-period standard deviation)
# 
# Lower Band = Middle Band - ( y *n-period standard deviation)
# 
# Where:
# 
# n = number of periods
# y = factor to apply to the standard deviation value, (typical default for y = 2)
# Detailed:
# 
# Calculate the moving average.
#  The formula is:
# d = ((P1-MA)^2 + (P2-MA)^2 + ... (Pn-MA)^2)/n
# 
# Pn is the price you pay for the nth interval n is the number of periods you select Subtract the moving average from each of the individual data points used in the moving average calculation. This gives you a list of deviations from the average. Square each deviation and add them all together. Divide this sum by the number of periods you selected.
# 
# Take the square root of d. This gives you the standard deviation.
# 
# delta = sqrt(d)
# 
# Compute the bands by using the following formulas:
# Upper Band = MA + delta
# Middle Band = MA
# Lower Band = MA - delta

# In[30]:


for close_price in close:
    history.append(close_price)
    if len(history) > time_period: # we only want to maintain at most 'time_period' number of price observations
        del(history[0])
        
    sma = stats.mean(history)
    sma_values.append(sma) # simple moving average or middle band
    variance = 0 # variance is the square of standard deviation
    for hist_price in history:
        variance = variance + ((hist_price - sma)**2)
        
    # use square root to get standard deviation
    stdev = math.sqrt(variance / len(history))
    
    upper_band.append(sma + stdev_factor * stdev)
    lower_band.append(sma - stdev_factor * stdev)
        


# In[31]:


nvda_data = nvda_data.assign(
    ClosePrice=pd.Series(close[:len(nvda_data.index)], index=nvda_data.index))
nvda_data = nvda_data.assign(
    MiddleBollingerBand20DaySMA=pd.Series(sma_values, index=nvda_data.index))
nvda_data = nvda_data.assign(UpperBollingerBand20DaySMA2StdevFactor=pd.Series(
    upper_band[:len(nvda_data.index)], index=nvda_data.index))
nvda_data = nvda_data.assign(LowerBollingerBand20DaySMA2StdevFactor=pd.Series(
    lower_band[:len(nvda_data.index)], index=nvda_data.index))


# In[32]:


close_price = nvda_data['ClosePrice']
mband = nvda_data['MiddleBollingerBand20DaySMA']
uband = nvda_data['UpperBollingerBand20DaySMA2StdevFactor']
lband = nvda_data['LowerBollingerBand20DaySMA2StdevFactor']


# In[33]:


fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='NVIDIA price in $')
close_price.plot(ax=ax1, color='g', lw=2., legend=True)
mband.plot(ax=ax1, color='b', lw=2., legend=True)
uband.plot(ax=ax1, color='black', lw=2., legend=True)
lband.plot(ax=ax1, color='r', lw=2., legend=True)
plt.show()


# # Thank you!
