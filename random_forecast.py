import numpy as np
import pandas as pd
import quandl

from backtest import Strategy, Portfolio

class RandomForecastingStrategy(Strategy):
    "Derives from strategy to produce a set of signals that are randomly generated shorts/longs. Nonsensical strategy, but acceptable for demonstrating backtesting structure"
    
    def __init__(self, symbol, bars):
        "Requires symbol ticker and pandas DF of bars"
        self.symbol = symbol
        self.bars = bars
        
    def generate_signals(self):
        "Creates pandas dataframe of random signals"
        signals = pd.DataFrame(index = self.bars.index)
        signals['signal'] = np.sign(np.random.randn(len(signals)))
        signals['signal'][0:5] = 0.0
        return signals
    
class MarketOnOpenPortfolio(Portfolio):
    """Inherits portfolio to create system that purchases 100 units of a ticker symbol upon a long or short signal, assuming open price of bar.
    Zero trans. costs and cash immediately borrowed (no margin posting or interest).
    
    Requires:
    symbol = stock symbol
    bars = DF of bars for a symbol set
    signals = DF of signals (1,0,-1)
    initial_capital = amount in cash at start of portfolio
     
    """
    
    def __init__(self, symbol, bars, signals, initial_capital = 100000.0):
        self.symbol = symbol
        self.bars = bars
        self.signals = signals
        self.inital_capital = float(initial_capital)
        self.positions = self.generate_positions()
        
    def generate_positions(self):
        """Creates a 'positions' DF that simply longs or shorts 100 of the symbol based on forecast signals of {-1,0,1} from signals DF."""
        
        positions = pd.DataFrame(index = signals.index).fillna(0.0)
        positions[self.symbol] = 100*signals['signal']
        return positions
    
    def backtest_portfolio(self):
        """Constructs portfolio from positions DF by assuming ability to trade @ a precise market open price of each bar. Calculates total cash and holdings to generate an equity curve and a set of bar-based returns"""
        
        portfolio = self.positions*self.bars['Open']
        pos_diff = self.positions.diff()
        
        portfolio['holdings'] = (self.positions*self.bars['Open']).sum(axis = 1)
        portfolio['cash'] = self.initial_capital - (pos_diff*self.bars['Open']).sum(axis = 1).cumsum()
        
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        
        return Portfolio