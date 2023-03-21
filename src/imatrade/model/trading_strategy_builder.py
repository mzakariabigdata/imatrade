"""
Contient les classes Builder (MACrossoverStrategyBuilder, RSIStrategyBuilder)
"""
from abc import ABC, abstractmethod
from .trading_strategy import MACrossoverStrategy, RSIStrategy

class TradingStrategyBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class MACrossoverStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.short_window = None
        self.long_window = None

    def set_short_window(self, short_window):
        self.short_window = short_window
        return self

    def set_long_window(self, long_window):
        self.long_window = long_window
        return self

    def build(self, config):
        return MACrossoverStrategy(short_window=config["short_window"], long_window=config["long_window"])


class RSIStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.rsi_period = None
        self.overbought = None
        self.oversold = None

    def set_rsi_period(self, rsi_period):
        self.rsi_period = rsi_period
        return self

    def set_overbought(self, overbought):
        self.overbought = overbought
        return self

    def set_oversold(self, oversold):
        self.oversold = oversold
        return self

    def build(self, config):
        return RSIStrategy(rsi_period=config["rsi_period"], oversold=config["oversold"], overbought=config["overbought"])
