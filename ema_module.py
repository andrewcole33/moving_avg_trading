import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from functools import reduce
import datetime
import numpy as np

sns.set(style = 'darkgrid', context = 'talk', palette = 'Dark2')

import warnings
warnings.filterwarnings('ignore')



def grab_portfolio_data(tickers, start, end):
    
    """This function will utilize the yahoo finance (yfinance) API to gather historical equity data for your portfolio. Pass an equity ticker, or a list of them, as well as your beginning and end dates to create a resulting pandas dataframe with respective closing prices of each asset.
    
    Parameters
    ----------
    - tickers: str; Either a singular or list of equity ticker symbols to gather
          ex: Singular Equity TESLA -> "TSLA"
          ex: Multiple Equities TESLA, APPLE, FORD -> ["TSLA", "AAPL", "F"]
          
    - start: str; The first date that you want to grab data from (Format: "YYYY-MM-DD").
          ex: "2015-01-01"
          
    - end: str; The last date that you want to grab data from (Format: "YYYY-MM-DD").
          ex: "2020-03-21"
    """
    
    yf.pdr_override()
    date_format = mdates.DateFormatter('%m/%y')
    df = pdr.get_data_yahoo(tickers, start = start, end = end, interval = '1d')
    df = df.Close
    
    return df
    
    
    

def view_asset_history(df, ticker, short_window, long_window):
    
    short_rolling = df.rolling(window = short_window).mean()
    long_rolling = df.rolling(window = long_window).mean()
    
    fig, ax = plt.subplots(figsize = (20, 10))
    sma_plot = sns.lineplot(df.index, df[f"{ticker}"], label = f"{ticker} Close Price")
    sma_plot = sns.lineplot(short_rolling.index, short_rolling[f"{ticker}"], label = f"{ticker} {short_window}-day SMA")
    sma_plot = sns.lineplot(long_rolling.index, long_rolling[f"{ticker}"], label = f"{ticker} {long_window}-day SMA")
    sma_plot.set_title('Portfolio Simple Moving Averages', fontweight = 'bold', fontsize = 20)
    
    ema_short = df.ewm(span = short_window, adjust = False).mean()
    
    fig, ax = plt.subplots(figsize = (20, 10))
    ema_plot = sns.lineplot(df.index, df[f"{ticker}"], label = f"{ticker} Close Price")
    ema_plot = sns.lineplot(ema_short.index, ema_short[f"{ticker}"], label = f"{ticker} EMA: {short_window} days")
    ema_plot = sns.lineplot(short_rolling.index, short_rolling[f"{ticker}"], label = f"{ticker} SMA: {short_window} days")
    ema_plot.set_title('Portfolio Exponential vs. Simple Moving Averages', fontweight = 'bold', fontsize = 20)
    
    
    trade_pos_raw = df - ema_short
    trade_positions = trade_pos_raw.apply(np.sign) * 1/(len(df.columns))
    trading_pos_final = trade_positions.shift(1)

    
    return sma_plot, ema_plot

    
