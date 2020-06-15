from abc import ABCMeta, abstractmethod




class Strategy(object):
    """Abstract base class which will provide space for following trading strategies"""
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def generate_signals(self):
        """Implementation is required to return DF trade signals (long, short, hold (1, -1, 0))"""
        
        raise NotImplementedError("Should implement generate_signals()!")
        
        
    
        
    