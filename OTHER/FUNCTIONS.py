#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# math file 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import matplotlib
import xlrd
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from pmdarima.arima import auto_arima
from pmdarima.arima import ADFTest
from sklearn.metrics import r2_score
from pmdarima.arima import ndiffs
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.plotting import autocorrelation_plot, lag_plot
import itertools
import statsmodels.api as sm
from matplotlib.pylab import rcParams
plt.style.use('ggplot')
from statsmodels.tsa.stattools import adfuller
from collections import Counter
import seaborn as sns

def plot_acf_pacf(ts, figsize=(10,8), lags = 24, agency = 'add'):
    '''Plots the ACF and PACF of the time series.'''
    fig,ax = plt.subplots(nrows=3,
                         figsize = figsize)
    
    #plot time series
    ts.plot(ax=ax[0])
    
    #plot acf, pacf
    plot_acf(ts,ax=ax[1], lags=lags)
    plot_pacf(ts, ax=ax[2], lags=lags)
    fig.tight_layout()
    
    fig.suptitle(f'Agency: {agency}',y=1.1, fontsize=20)
    
    for a in ax[1:]:
        a.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(min_n_ticks=lags, integer = True))
        a.xaxis.grid()
    return fig,ax


def dftest(df):
    ''' This function will test a dataframe to determine stationarity'''
    dftest = adfuller(df.dropna(), autolag = 'AIC')

    print("1. ADF : ",dftest[0])
    print("2. P-Value : ", dftest[1])
    print("3. Num Of Lags : ", dftest[2])
    print("4. Num Of Observations Used For ADF Regression and Critical Values Calculation :", dftest[3])
    print("5. Critical Values :")
    for key, val in dftest[4].items():
        print("\t",key, ": ", val)
        
def concat_calls(forecast_diff, difference_twenty, actual_diff):
    ''' This function labels and concatenates the forecasted and actual calls to format for a barplot'''
    forecast_diff = difference_twenty[['Date', 'forecast_calls', 'actual_calls']]
    forecast_diff['actual_calls'] = 'Forecast'
    forecast_diff.rename(columns = {'actual_calls' : 'type', 'forecast_calls':'calls'}, inplace = True)
    actual_diff = difference_twenty[['Date', 'forecast_calls', 'actual_calls']]
    actual_diff['forecast_calls'] = 'actual'
    actual_diff.rename(columns={'forecast_calls':'type', 'actual_calls':'calls'}, inplace = True)
    whole_df = pd.concat([actual_diff, forecast_diff])
    return whole_df.head()

def plot_bars(df, agency):    
    ''' This function creates a barplot comparing actual versus forecasted calls'''
    ax = sns.barplot(x="Date", y="calls", hue="type", data= df)
    ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept', 'Oct', 'Nov', 'Dec'])
    ax.set_title(agency + ': Actual Versus Forecasted')
    plt.show()
    
    
def dynamic_forecast(df, dpw_20, agency, pred_dynamic, pred_dynamic_conf, val_forecasted): 
    
    ''' This function plots the dynamic forecast of the agency queue.'''
    
    
    ax = df['2015':].plot(label='observed', figsize=(20, 15))
    pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)
    dpw_20['2019':].plot(label= 'Actual_2020_Calls', ax = ax)

    ax.fill_between(pred_dynamic_conf.index,
                    pred_dynamic_conf.iloc[:, 0],
                    pred_dynamic_conf.iloc[:, 1], color='g', alpha=.3)

    ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2020-12-31'), val_forecasted.index[-1], alpha=.1, zorder=-1)

    ax.set_xlabel('Date')
    ax.set_ylabel('Median Home Values')

    labels = {'2020_Calls', 'Agency_Calls', '2020_Forecast'}

    plt.legend(labels, loc = 'upper left', fontsize = 'xx-large')
    plt.title(agency, fontdict = {'fontsize':36})
    plt.show()

    
    
def see_confidence_int(df, dpw_20, agency, prediction, pred_conf):
    ''' This function plots the confidence interval visualization.'''
    ax = df.plot(label='observed', figsize=(20, 15))
    dpw_20['2019':].plot(label= 'Actual_2020_Calls', ax = ax)
    prediction.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_conf.index,
                    pred_conf.iloc[:, 0],
                    pred_conf.iloc[:, 1], color='k', alpha=0.25)
    ax.set_xlabel('Date', fontdict={'fontsize' : 24})
    ax.set_ylabel('Queue Requests', fontdict={'fontsize' : 24})
    ax.set_title(agency, fontdict={'fontsize' : 30})
    new = ['Agency_Calls', '2020_Calls', '2020_Forecast']

    plt.legend(labels = new, loc = 'upper left', fontsize = 'xx-large')
    plt.show()

