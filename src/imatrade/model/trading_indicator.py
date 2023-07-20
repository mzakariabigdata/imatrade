"""
Contient les classes d'indicators
"""
from abc import ABC, abstractmethod
from typing import List
import pandas as pd
from ta.momentum import RSIIndicator as RSI
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.trend import MACD
from ta.volatility import AverageTrueRange
from pandas_ta.momentum import rsi


# from ta.trend import IchimokuIndicator
import numpy as np
from imobject import ObjDict


class TradingIndicator(ABC):  # pylint: disable=too-few-public-methods
    """Classe de base abstraite pour les indicateurs de trading."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.name = kwargs.name
        self.description = kwargs.description
        self.display_name = kwargs.display_name
        self.parameters = kwargs.parameters

    @abstractmethod
    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur pour une barre donnée."""

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"


class IchimokuCloudIndicator(TradingIndicator):
    """Classe pour l'indicateur Ichimoku Cloud."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "Ichimoku Cloud Indicator"
        kwargs.description = (
            " Une stratégie basée sur l'indicateur Ichimoku Kinko Hyo (nuage d'Ichimoku), "
            "qui combine plusieurs moyennes mobiles pour identifier"
            " la tendance et les niveaux de support/résistance."
        )
        super().__init__(**kwargs)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        return super().prepare_indicator_data_for_bar(window_data)

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Ichimoku Cloud."""
        self.market_data = market_data.copy()

        # Calculer la conversion line
        high_values = (
            self.market_data["high"]
            .rolling(window=self.parameters["conversion_line_period"])
            .max()
        )
        low_values = (
            self.market_data["low"]
            .rolling(window=self.parameters["conversion_line_period"])
            .min()
        )
        self.market_data["conversion_line"] = (high_values + low_values) / 2

        # Calculer la base line
        high_values = (
            self.market_data["high"]
            .rolling(window=self.parameters["base_line_period"])
            .max()
        )
        low_values = (
            self.market_data["low"]
            .rolling(window=self.parameters["base_line_period"])
            .min()
        )
        self.market_data["base_line"] = (high_values + low_values) / 2

        # Calculer la lagging span
        self.market_data["lagging_span"] = self.market_data["close"].shift(
            self.parameters["displacement"]
        )

        # Calculer la senkou span A
        senkou_span_a = (
            (self.market_data["conversion_line"] + self.market_data["base_line"]) / 2
        ).shift(self.parameters["displacement"])
        self.market_data["senkou_span_a"] = senkou_span_a

        # Calculer la senkou span B
        high_values = (
            self.market_data["high"]
            .rolling(window=self.parameters["lagging_span_periods"])
            .max()
        )
        low_values = (
            self.market_data["low"]
            .rolling(window=self.parameters["lagging_span_periods"])
            .min()
        )
        self.market_data["senkou_span_b"] = ((high_values + low_values) / 2).shift(
            self.parameters["displacement"]
        )
        self.market_data = self.market_data.dropna()
        return self.market_data


class ATRIndicator(TradingIndicator):
    """Classe pour l'indicateur Average True Range."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "ATR Indicator"
        kwargs.description = (
            "Une stratégie basée sur l'indicateur Average True Range (ATR), "
            "qui mesure la volatilité du marché en utilisant les bandes de Bollinger."
        )
        super().__init__(**kwargs)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        return super().prepare_indicator_data_for_bar(window_data)

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Average True Range."""
        self.market_data = market_data.copy()
        atr = AverageTrueRange(
            self.market_data["high"],
            self.market_data["low"],
            self.market_data["close"],
            window=self.parameters["window"],
        )
        self.market_data["atr"] = atr.average_true_range()
        self.market_data = self.market_data.dropna()
        return self.market_data


class MACDIndicator(TradingIndicator):
    """Classe pour l'indicateur Moving Average Convergence Divergence."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "MACD Indicator"
        kwargs.description = (
            "Une stratégie basée sur l'indicateur Moving Average Convergence"
            " Divergence (MACD), qui mesure la différence entre "
            "deux moyennes mobiles exponentielles."
        )
        super().__init__(**kwargs)

    def get_window_size(self):
        """Récupère la taille de la fenêtre."""
        return max(self.parameters["long_window"], self.parameters["short_window"])

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur MACD pour une barre donnée."""
        result = {}
        if len(window_data) >= self.get_window_size():
            macd = MACD(
                pd.Series(window_data),
                window_slow=self.parameters["long_window"],
                window_fast=self.parameters["short_window"],
                window_sign=self.parameters["signal_window"],
            )
            result["line"] = macd.macd().iloc[-1]
            result["signal"] = macd.macd_signal().iloc[-1]
            result["diff"] = macd.macd_diff().iloc[-1]
            print("result", result)
        return result if result else None


class MACrossoverIndicator(TradingIndicator):
    """Classe pour l'indicateur Moving Average Crossover."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.long_window = kwargs.parameters["long_window"]
        self.short_window = kwargs.parameters["short_window"]
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "Moving Average Crossover Indicator"
        kwargs.description = (
            "Une stratégie basée sur le croisement de deux moyennes mobiles."
        )
        super().__init__(**kwargs)

    def get_window_size(self):
        """Récupère la taille de la fenêtre."""
        return max(self.long_window, self.short_window)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Calculate short and long moving averages for given window data."""
        if len(window_data) < self.long_window:
            return None  # Not enough data to calculate long moving average
        if len(window_data) < self.short_window:
            return None  # Not enough data to calculate short moving average

        long_ma = np.mean(window_data[-self.long_window :])
        short_ma = np.mean(window_data[-self.short_window :])

        return (
            short_ma - long_ma
        )  # Return the difference between the short and long moving averages

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Moving Average Crossover."""
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
        self.market_data = self.market_data.dropna()
        return self.market_data


class RSIIndicator(TradingIndicator):
    """Classe pour l'indicateur Relative Strength Index."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.rsi_period = kwargs.parameters["rsi_period"]
        self.overbought = kwargs.parameters["overbought"]
        self.oversold = kwargs.parameters["oversold"]
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "RSI Indicator"
        kwargs.description = (
            "Une stratégie basée sur l'indicateur Relative Strength Index (RSI), qui "
            "mesure la force relative d'une action par rapport à son historique."
        )
        super().__init__(**kwargs)

    def get_window_size(self):
        """Récupère les données pour la fenêtre."""
        return self.rsi_period

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Calcule le RSI pour une liste donnée de prix."""
        result = {}
        if len(window_data) >= self.get_window_size():
            rsi_indicator = RSI(
                close=pd.Series(window_data), window=self.parameters["rsi_period"]
            )
            result["value"] = rsi_indicator.rsi().iloc[-1]
            result["oversold"] = self.parameters["oversold"]
        # self.market_data["RSI"] = rsi_indicator.rsi()
        return result if result else None

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Relative Strength Index."""
        self.market_data = market_data.copy()
        rsi_indicator = RSI(
            close=self.market_data["close"], window=self.parameters["rsi_period"]
        )
        self.market_data["RSI"] = rsi_indicator.rsi()

        self.market_data = self.market_data.dropna()
        return self.market_data


class BollingerBandsIndicator(TradingIndicator):
    """Classe pour l'indicateur Bollinger Bands."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "Bollinger Bands Indicator"
        kwargs.description = (
            "Une stratégie basée sur les bandes de Bollinger, "
            "qui sont des bandes de volatilité autour d'une moyenne mobile."
        )
        super().__init__(**kwargs)

    def get_window_size(self):
        """Récupère la taille de la fenêtre."""
        return self.parameters["window"]

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur Bollinger Bands pour une barre donnée."""
        result = {}
        if len(window_data) >= self.get_window_size():
            bolband = BollingerBands(
                close=pd.Series(window_data),
                window=self.parameters["window"],
                window_dev=self.parameters["num_std"],
            )
            bollinger_hband = bolband.bollinger_hband()
            bollinger_lband = bolband.bollinger_lband()
            if not bollinger_hband.empty:
                result["hband"] = bollinger_hband.iloc[-1]  # Return the last value
            if not bollinger_lband.empty:
                result["lband"] = bollinger_lband.iloc[-1]  # Return the last value
            # if not bollinger_hband.empty:
            #     return bollinger_hband.iloc[-1]  # Return the last value
        # return None
        return result if result else None

    def get_prepare_data(self):
        """Prépare les données pour l'indicateur Bollinger Bands."""
        return self.market_data

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Bollinger Bands."""
        self.market_data = market_data.copy()
        bollinger = BollingerBands(
            close=self.market_data["close"],
            window=self.parameters["window"],
            window_dev=self.parameters["num_std"],
        )
        self.market_data["bollinger_high"] = bollinger.bollinger_hband()
        self.market_data["bollinger_low"] = bollinger.bollinger_lband()
        self.market_data = self.market_data.dropna()
        return self.market_data


class StochasticOscillatorIndicator(TradingIndicator):
    """Classe pour l'indicateur Stochastic Oscillator."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "Stochastic Oscillator Indicator"
        kwargs.description = (
            "Une stratégie basée sur l'indicateur Stochastic Oscillator, qui"
            " mesure la force relative d'une action par rapport à son historique"
        )
        super().__init__(**kwargs)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        return super().prepare_indicator_data_for_bar(window_data)
    
    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Stochastic Oscillator."""
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
        self.market_data = self.market_data.dropna()
        return self.market_data


class RSIDivergenceIndicator(TradingIndicator):
    """Classe pour l'indicateur RSI Divergence."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "RSI Divergence Indicator"
        kwargs.description = (
            "Une stratégie basée sur les divergences de RSI, "
            "qui sont des divergences entre les prix et l'indicateur RSI."
        )
        super().__init__(**kwargs)

    def get_window_size(self):
        """Récupère la taille de la fenêtre."""
        return self.parameters["signal_period"]

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur RSI Divergence pour une barre donnée."""
        signal_period = self.parameters["signal_period"]
        long_rsi_period = self.parameters["long_rsi_period"]
        short_rsi_period = self.parameters["short_rsi_period"]

        if len(window_data) < max(signal_period, long_rsi_period, short_rsi_period):
            return None

        rsi_long = rsi(np.array(window_data), length=long_rsi_period).iloc[-1]
        rsi_short = rsi(np.array(window_data), length=short_rsi_period).iloc[-1]

        return rsi_long - rsi_short

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur RSI Divergence."""
        self.market_data = market_data.copy()
        rsi_indic = RSI(
            self.market_data["close"], window=self.parameters["signal_period"]
        )
        self.market_data["rsi"] = rsi_indic.rsi()
        self.market_data = self.market_data.dropna()
        return self.market_data


class MAEnvelopeIndicator(TradingIndicator):
    """Classe pour l'indicateur MA Envelope."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "MA Envelope Indicator"
        kwargs.description = (
            "Une stratégie basée sur l'enveloppe de moyenne mobile, qui est "
            "une moyenne mobile avec des bandes supérieure et inférieure."
        )
        super().__init__(**kwargs)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur MA Envelope pour une barre donnée."""
        result = {}
        if len(window_data) >= self.parameters["ma_period"]:
            ma = np.mean(window_data[-self.parameters["ma_period"] :])
            result["ma"] = ma
            result["price"] = window_data[-1]
            result["upper_band"] = ma * (1 + self.parameters["ma_distance"])
            result["lower_band"] = ma * (1 - self.parameters["ma_distance"])
        return result if result else None

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur MA Envelope."""
        self.market_data = market_data.copy()
        self.market_data["ma"] = self.moving_average(
            self.market_data["close"], self.parameters["ma_period"]
        )
        self.market_data["upper_band"] = self.market_data["ma"] * (
            1 + self.parameters["ma_distance"]
        )
        self.market_data["lower_band"] = self.market_data["ma"] * (
            1 - self.parameters["ma_distance"]
        )
        self.market_data = self.market_data.dropna()
        return self.market_data

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


class BreakoutIndicator(TradingIndicator):
    """Classe pour l'indicateur Breakout."""

    def __init__(self, **kwargs):
        kwargs = ObjDict(kwargs)
        self.market_data = None
        self.parameters = kwargs.parameters
        self.name = kwargs.name
        kwargs.display_name = "Breakout Indicator"
        kwargs.description = (
            "Une stratégie basée sur les ruptures de prix, qui sont des "
            "ruptures de prix au-dessus ou en dessous d'une moyenne mobile."
        )
        super().__init__(**kwargs)

    def prepare_indicator_data_for_bar(self, window_data: List[float]):
        """Prépare les données pour l'indicateur Breakout pour une barre donnée."""
        result = {}
        if len(window_data) >= self.parameters["window"]:
            ma = np.mean(window_data[-self.parameters["window"] :])
            result["ma"] = ma
            result["price"] = window_data[-1]
            result["breakout"] = window_data[-1] > ma
        return result if result else None

    def prepare_data(self, market_data):
        """Prépare les données pour l'indicateur Breakout."""
        self.market_data = market_data.copy()
        self.market_data = self.market_data.dropna()
        return self.market_data
