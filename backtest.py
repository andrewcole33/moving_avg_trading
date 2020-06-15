from abc import ABCMeta, abstractmethod




class Strategy(object):
    """Abstract base class which will provide space for following trading strategies."""
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_signals(self):
        """Implementation is required to return DF trade signals (long, short, hold (1, -1, 0))."""
        
        raise NotImplementedError("Should implement generate_signals()!")
        
        
    
        
    
class Portfolio(object):
    """Abstract base class representing portfolio of positions, determined on basis of a set of signals provided by a Strategy."""
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_positions(self):
        "This will give the logic for determining how portfolio positions are allocatied on the basis of forecasting signals and available capital."
        
        raise NotImplementedError("Should implement generate_positions()!")
        
    @abstractmethod
    def backtest_portfolio(self):
        "Give logic for creating trade orders and following equity growth curve as a sum of holdings and capital, and the bar-period returns from the 'positions' dataframe.
        
        raise NotImplementedError("Should implement backtest_portfolio()!")