"""
Contient les classes de stratégie (MACrossoverStrategy, RSIStrategy)
"""
from abc import ABC, abstractmethod
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
from ta.trend import IchimokuIndicator
import numpy as np
from imobject import ObjDict

class TradingStrategy(ABC):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.name = kwargs.name
        self.description = kwargs.description
        self.display_name = kwargs.display_name
        self.parameters = kwargs.parameters

    @abstractmethod
    def execute(self):
        pass



class IchimokuCloudStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()

        # Calculer la conversion line
        high_values = self.market_data["high"].rolling(window=self.parameters["conversion_line_period"]).max()
        low_values = self.market_data["low"].rolling(window=self.parameters["conversion_line_period"]).min()
        self.market_data["conversion_line"] = (high_values + low_values) / 2

        # Calculer la base line
        high_values = self.market_data["high"].rolling(window=self.parameters["base_line_period"]).max()
        low_values = self.market_data["low"].rolling(window=self.parameters["base_line_period"]).min()
        self.market_data["base_line"] = (high_values + low_values) / 2

        # Calculer la lagging span
        self.market_data["lagging_span"] = self.market_data["close"].shift(self.parameters["displacement"])

        # Calculer la senkou span A
        senkou_span_a = ((self.market_data["conversion_line"] + self.market_data["base_line"]) / 2).shift(
            self.parameters["displacement"]
        )
        self.market_data["senkou_span_a"] = senkou_span_a

        # Calculer la senkou span B
        high_values = self.market_data["high"].rolling(window=self.parameters["lagging_span_periods"]).max()
        low_values = self.market_data["low"].rolling(window=self.parameters["lagging_span_periods"]).min()
        self.market_data["senkou_span_b"] = ((high_values + low_values) / 2).shift(self.parameters["displacement"])

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Calculer les signaux pour les positions longues et courtes
        signals["long_signal"] = (
            self.market_data["lagging_span"] > self.market_data["senkou_span_a"]
        ) & (self.market_data["close"] > self.market_data["senkou_span_b"])
        signals["short_signal"] = (
            self.market_data["lagging_span"] < self.market_data["senkou_span_a"]
        ) & (self.market_data["close"] < self.market_data["senkou_span_b"])

        # Combiner les signaux pour obtenir la position totale
        signals.loc[signals["long_signal"] == True, "signal"] = 1.0
        signals.loc[signals["short_signal"] == True, "signal"] = -1.0

        return signals
    
    def execute(self):
        print(f"Executing Ichimoku Cloud strategy with conversion line period {self.parameters['conversion_line_period']}, base line period {self.parameters['base_line_period']}, lagging span periods {self.parameters['lagging_span_periods']}, and displacement {self.parameters['displacement']}")


class ATRStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        atr = AverageTrueRange(
            self.market_data["high"],
            self.market_data["low"],
            self.market_data["close"],
            window=self.parameters["window"],
        )
        self.market_data["atr"] = atr.average_true_range()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Vous pouvez définir vos propres règles de signal en utilisant la colonne ATR de self.market_data
        # Par exemple, vous pouvez créer des signaux basés sur des niveaux d'ATR spécifiques
        sig_start = self.parameters["window"]
        sig_end = len(self.market_data)

        atr_values = self.market_data["atr"].iloc[sig_start:sig_end].values

        # Vous pouvez ajuster les seuils selon votre stratégie de trading
        # signals_array = np.where(atr_values > self.parameters["upper_threshold"], 1.0, 0.0)
        signals.iloc[sig_start:sig_end, 0]
        return signals
    
    def execute(self):
        print(f"Executing ATR strategy with window {self.parameters['window']}")


class MACDStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        macd = MACD(
            self.market_data["close"],
            window_slow=self.parameters["long_window"],
            window_fast=self.parameters["short_window"],
            window_sign=self.parameters["signal_window"],
        )
        self.market_data["macd"] = macd.macd()
        self.market_data["macd_signal"] = macd.macd_signal()
        self.market_data["macd_diff"] = macd.macd_diff()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Create a signal when the MACD crosses the signal line
        sig_start = self.parameters["long_window"]
        sig_end = len(self.market_data)

        macd_diff = self.market_data["macd_diff"].iloc[sig_start:sig_end].values

        signals_array = np.where(macd_diff > 0, 1.0, 0.0)
        signals.iloc[sig_start:sig_end, 0] = signals_array

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["positions"] = signals["signal"].diff()

        return signals
    
    def execute(self):
        print(
            f"Executing MACD strategy with short window {self.parameters['short_window']}, long window {self.parameters['long_window']}, and signal window {self.parameters['signal_window']}"
        )
    


class MACrossoverStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        self.market_data["short_mavg"] = (
            self.market_data["close"]
            .rolling(window=self.parameters["short_window"])
            .mean()
        )
        self.market_data["long_mavg"] = (
            self.market_data["close"]
            .rolling(window=self.parameters["long_window"])
            .mean()
        )

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
        print(
            f"Executing Moving Average Crossover strategy with short window {self.short_window} and long window {self.long_window}"
        )


class RSIStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        rsi_indicator = RSIIndicator(
            close=self.market_data["close"], window=self.parameters["rsi_period"]
        )
        self.market_data["RSI"] = rsi_indicator.rsi()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Generate buy signal when RSI is below the oversold threshold
        sig_start = self.parameters["rsi_period"]
        sig_end = len(self.market_data)

        signals.iloc[sig_start:sig_end]["signal"] = np.where(
            self.market_data["RSI"].iloc[sig_start:sig_end]
            < self.parameters["oversold"],
            1.0,
            0.0,
        )

        # Generate sell signal when RSI is above the overbought threshold
        signals.iloc[sig_start:sig_end]["signal"] = np.where(
            self.market_data["RSI"].iloc[sig_start:sig_end]
            > self.parameters["overbought"],
            -1.0,
            signals["signal"].iloc[sig_start:sig_end],
        )

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["orders"] = signals["signal"].diff()

        return signals

    def execute(self):
        print(
            f"Executing RSI strategy with RSI period {self.rsi_period}, overbought at {self.overbought} and oversold at {self.oversold}"
        )


class BollingerBandsStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        bollinger = BollingerBands(
            close=self.market_data["close"],
            window=self.parameters["window"],
            window_dev=self.parameters["num_std"],
        )
        self.market_data["bollinger_high"] = bollinger.bollinger_hband()
        self.market_data["bollinger_low"] = bollinger.bollinger_lband()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        signals["signal"][
            self.market_data["close"] < self.market_data["bollinger_low"]
        ] = 1.0
        signals["signal"][
            self.market_data["close"] > self.market_data["bollinger_high"]
        ] = -1.0

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["positions"] = signals["signal"].diff()

        return signals

    def execute(self):
        print(
            f"Executing Bollinger Bands strategy with window {self.parameters['window']} and {self.parameters['num_std']} standard deviations"
        )


class StochasticOscillatorStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        stochastic = StochasticOscillator(
            high=self.market_data["high"],
            low=self.market_data["low"],
            close=self.market_data["close"],
            window=self.parameters["k_window"],
            smooth_window=self.parameters["d_window"],
        )
        self.market_data["stoch_k"] = stochastic.stoch()
        self.market_data["stoch_d"] = stochastic.stoch_signal()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        signals["signal"][
            (self.market_data["stoch_k"] < self.parameters["oversold"])
            & (self.market_data["stoch_d"] < self.parameters["oversold"])
        ] = 1.0
        signals["signal"][
            (self.market_data["stoch_k"] > self.parameters["overbought"])
            & (self.market_data["stoch_d"] > self.parameters["overbought"])
        ] = -1.0

        # Calculate trading orders: 1 for buy, -1 for sell, 0 for holding
        signals["positions"] = signals["signal"].diff()

        return signals

    def execute(self):
        print(
            f"Executing Stochastic Oscillator strategy with K window {self.parameters['k_window']}, D window {self.parameters['d_window']}, oversold {self.parameters['oversold']}, and overbought {self.parameters['overbought']}"
        )


class RSIDivergenceStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        rsi = RSIIndicator(
            self.market_data["close"], window=self.parameters["signal_period"]
        )
        self.market_data["rsi"] = rsi.rsi()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Trouver les divergences en comparant les hauts/bas des prix et RSI
        price_highs = self.market_data["high"]
        rsi_highs = self.market_data["rsi"].rolling(window=2).max()
        bearish_divergence = price_highs < rsi_highs

        price_lows = self.market_data["low"]
        rsi_lows = self.market_data["rsi"].rolling(window=2).min()
        bullish_divergence = price_lows > rsi_lows

        # Marquer les signaux de divergence en utilisant les seuils de divergence spécifiés
        signals.loc[bearish_divergence & (self.market_data["rsi"] > self.parameters["short_rsi_period"]), "signal"] = -1.0
        signals.loc[bullish_divergence & (self.market_data["rsi"] < (100 - self.parameters["short_rsi_period"])), "signal"] = 1.0

        return signals

    def execute(self):
        print(f"Executing RSIDivergence  strategy with signal_period {self.parameters['signal_period']}, long_rsi_period {self.parameters['long_rsi_period']}, short_rsi_period {self.parameters['short_rsi_period']}")


class MAEnvelopeStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()
        self.market_data["ma"] = self.moving_average(self.market_data["close"], self.parameters["ma_period"])
        self.market_data["upper_band"] = self.market_data["ma"] * (1 + self.parameters["ma_distance"])
        self.market_data["lower_band"] = self.market_data["ma"] * (1 - self.parameters["ma_distance"])

    def moving_average(self, data, window):
        """
        Calcule la moyenne mobile d'une série de données avec une fenêtre donnée.
        
        Args:
        data (pd.Series): La série de données.
        window (int): La taille de la fenêtre.
        
        Returns:
        pd.Series: La série de la moyenne mobile.
        """
        return data.rolling(window=window).mean()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        # Acheter lorsque le prix touche la bande inférieure et vendre lorsque le prix touche la bande supérieure
        signals.loc[self.market_data["close"] < self.market_data["lower_band"], "signal"] = 1.0
        signals.loc[self.market_data["close"] > self.market_data["upper_band"], "signal"] = -1.0

        return signals

    def execute(self):
        print(f"Executing MAEnvelope  strategy with ma_period {self.parameters['ma_period']}, buy_margin {self.parameters['buy_margin']}, and sell_margin {self.parameters['sell_margin']}")


class BreakoutStrategy(TradingStrategy):
    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        super().__init__(**kwargs)

    def prepare_data(self, market_data):
        self.market_data = market_data.copy()

    def generate_signals(self):
        signals = pd.DataFrame(index=self.market_data.index)
        signals["signal"] = 0.0

        signals["rolling_max"] = self.market_data["high"].rolling(
            window=self.parameters["lookback_window"], min_periods=1
        ).max()

        signals["rolling_min"] = self.market_data["low"].rolling(
            window=self.parameters["lookback_window"], min_periods=1
        ).min()

        signals["buy_breakout"] = signals["rolling_max"] - self.market_data["close"] < (
            self.market_data["close"] * self.parameters["buy_margin"]
        )

        signals["sell_breakout"] = self.market_data["close"] - signals["rolling_min"] < (
            self.market_data["close"] * self.parameters["sell_margin"]
        )

        signals["signal"] = np.where(
            signals["buy_breakout"], 1.0, np.where(signals["sell_breakout"], -1.0, 0.0)
        )

        # Remove intermediate values of signal
        signals["positions"] = signals["signal"].diff()
        signals.iloc[0, -1] = signals["signal"].iloc[-1]
        return signals


    def execute(self):
        print(f"Executing Breakout strategy with lookback_window {self.parameters['lookback_window']}, buy_margin {self.parameters['buy_margin']}, and sell_margin {self.parameters['sell_margin']}")
