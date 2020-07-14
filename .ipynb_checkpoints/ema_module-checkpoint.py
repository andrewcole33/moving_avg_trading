import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from functools import reduce
import datetime

sns.set(style = 'darkgrid', context = 'talk', palette = 'Dark2')

import warnings
warnings.filterwarnings('ignore')



def grab_portfolio_data(tickers, start, end, interval, attribute, short_window, long_window):
    
    yf.pdr_override()
    date_format = mdates.DateFormatter('%m/%y')
    df = pdr.get_data_yahoo(tickers, start = start, end = end, interval = interval)
    df = df[f"{attribute}"]
    
    short_rolling = df.rolling(window = short_window).mean()
    long_rolling = df.rolling(window = long_window).mean()
    
    
    