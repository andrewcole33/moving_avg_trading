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



def grab_portfolio_data(tickers, start, end, interval, attribute):
    
    yf.pdr_override()
    date_format = mdates.DateFormatter('%m/%y')
    df = pdr.get_data_yahoo(tickers, start = start, end = end, interval = interval)
    df = df[f"{attribute}"]
    
    return df
    
    
    

def view_portfolio_history(df, ticker, short_window, long_window):
    
    short_rolling = df.rolling(window = short_window).mean()
    long_rolling = df.rolling(window = long_window).mean()
    
    fig, ax = plt.subplots(figsize = (20, 9))
    plot = sns.lineplot(df.index, df[f"{ticker}"], label = f"{ticker} Close Price")
    plot = sns.lineplot(short_rolling.index, short_rolling[f"{ticker}"], label = f"{ticker} {short_window}-day SMA")
    plot = sns.lineplot(long_rolling.index, long_rolling[f"{ticker}"], label = f"{ticker} {long_window}-day SMA")
    
    return plot