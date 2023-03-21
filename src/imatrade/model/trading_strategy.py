"""
Contient les classes de stratégie (MACrossoverStrategy, RSIStrategy)
"""
from abc import ABC, abstractmethod
import pandas as pd
from ta.momentum import RSIIndicator
import numpy as np

class TradingStrategy(ABC):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    @abstractmethod
    def execute(self):
        pass


class MACrossoverStrategy(TradingStrategy):
    def __init__(self, short_window, long_window):
        parameters = {"short_window": short_window, "long_window": long_window}
        super().__init__("Moving Average Crossover", parameters)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        self.market_data["short_mavg"] = self.market_data["close"].rolling(window=self.parameters["short_window"]).mean()
        self.market_data["long_mavg"] = self.market_data["close"].rolling(window=self.parameters["long_window"]).mean()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Create a signal when the short moving average crosses the long moving average
        sig_start = self.parameters["short_window"]
        sig_end = len(self.market_data)

        short_mavg = self.market_data["short_mavg"].iloc[sig_start:sig_end].values
        long_mavg = self.market_data["long_mavg"].iloc[sig_start:sig_end].values

        signals_array = np.where(short_mavg > long_mavg, 1.0, 0.0)
        signals.iloc[sig_start:sig_end, 0] = signals_array

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["positions"] = signals["signal"].diff()

        return signals
    
    def execute(self):
        print(f"Executing Moving Average Crossover strategy with short window {self.short_window} and long window {self.long_window}")



class RSIStrategy(TradingStrategy):
    def __init__(self, rsi_period, oversold, overbought):
        parameters = {"rsi_period": rsi_period, "oversold": oversold, "overbought": overbought}
        super().__init__("Relative Strength Index", parameters)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        rsi_indicator = RSIIndicator(close=self.market_data["close"], window=self.parameters["rsi_period"])
        self.market_data["RSI"] = rsi_indicator.rsi()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Generate buy signal when RSI is below the oversold threshold
        sig_start = self.parameters["rsi_period"]
        sig_end = len(self.market_data)

        signals.iloc[sig_start:sig_end]["signal"] = np.where(
            self.market_data["RSI"].iloc[sig_start:sig_end] < self.parameters["oversold"],
            1.0,
            0.0,
        )

        # Generate sell signal when RSI is above the overbought threshold
        signals.iloc[sig_start:sig_end]["signal"] = np.where(
            self.market_data["RSI"].iloc[sig_start:sig_end] > self.parameters["overbought"],
            -1.0,
            signals["signal"].iloc[sig_start:sig_end],
        )

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["orders"] = signals["signal"].diff()

        return signals


    def execute(self):
        print(f"Executing RSI strategy with RSI period {self.rsi_period}, overbought at {self.overbought} and oversold at {self.oversold}")
