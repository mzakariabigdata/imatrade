"""
Contient les classes Stategy
"""

from abc import ABC, abstractmethod


class TradingStrategy(ABC):  # pylint: disable=too-few-public-methods
    """Classe abstraite pour les stratégies de trading."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")

    @abstractmethod
    def execute(self):
        """Méthode abstraite pour exécuter la stratégie."""


class MACrossoverStrategy(TradingStrategy):
    """Stratégie de trading MACrossover"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fast_ma = kwargs.get("fast_ma", None)
        self.slow_ma = kwargs.get("slow_ma", None)

    def execute(self):
        """Exécute la stratégie de trading MACrossover"""
        print("Exécution de la stratégie MACrossover")
        print(f"Fast MA: {self.fast_ma}")
        print(f"Slow MA: {self.slow_ma}")

class RSIStrategy(TradingStrategy):
    """Stratégie de trading RSI"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rsi_period = kwargs.get("rsi_period", None)
        self.rsi_upper = kwargs.get("rsi_upper", None)
        self.rsi_lower = kwargs.get("rsi_lower", None)

    def execute(self):
        """Exécute la stratégie de trading RSI"""
        print("Exécution de la stratégie RSI")
        print(f"RSI period: {self.rsi_period}")
        print(f"RSI upper: {self.rsi_upper}")
        print(f"RSI lower: {self.rsi_lower}")

class StochasticStrategy(TradingStrategy):
    """Stratégie de trading Stochastic"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stochastic_period = kwargs.get("stochastic_period", None)
        self.stochastic_upper = kwargs.get("stochastic_upper", None)
        self.stochastic_lower = kwargs.get("stochastic_lower", None)

    def execute(self):
        """Exécute la stratégie de trading Stochastic"""
        print("Exécution de la stratégie Stochastic")
        print(f"Stochastic period: {self.stochastic_period}")
        print(f"Stochastic upper: {self.stochastic_upper}")
        print(f"Stochastic lower: {self.stochastic_lower}")

class BollingerBandsStrategy(TradingStrategy):
    """Stratégie de trading BollingerBands"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bollinger_bands_period = kwargs.get("bollinger_bands_period", None)
        self.bollinger_bands_upper = kwargs.get("bollinger_bands_upper", None)
        self.bollinger_bands_lower = kwargs.get("bollinger_bands_lower", None)

    def execute(self):
        """Exécute la stratégie de trading BollingerBands"""
        print("Exécution de la stratégie BollingerBands")
        print(f"BollingerBands period: {self.bollinger_bands_period}")
        print(f"BollingerBands upper: {self.bollinger_bands_upper}")
        print(f"BollingerBands lower: {self.bollinger_bands_lower}")

class RSIDivergenceStrategy(TradingStrategy):
    """Stratégie de trading RSIDivergence"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rsi_period = kwargs.get("rsi_period", None)
        self.rsi_upper = kwargs.get("rsi_upper", None)
        self.rsi_lower = kwargs.get("rsi_lower", None)

    def execute(self):
        """Exécute la stratégie de trading RSIDivergence"""
        print("Exécution de la stratégie RSIDivergence")
        print(f"RSI period: {self.rsi_period}")
        print(f"RSI upper: {self.rsi_upper}")
        print(f"RSI lower: {self.rsi_lower}")

class StochasticOscillatorStrategy(TradingStrategy):
    """Stratégie de trading StochasticOscillator"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stochastic_oscillator_period = kwargs.get("stochastic_oscillator_period", None)
        self.stochastic_oscillator_upper = kwargs.get("stochastic_oscillator_upper", None)
        self.stochastic_oscillator_lower = kwargs.get("stochastic_oscillator_lower", None)

    def execute(self):
        """Exécute la stratégie de trading StochasticOscillator"""
        print("Exécution de la stratégie StochasticOscillator")
        print(f"StochasticOscillator period: {self.stochastic_oscillator_period}")
        print(f"StochasticOscillator upper: {self.stochastic_oscillator_upper}")
        print(f"StochasticOscillator lower: {self.stochastic_oscillator_lower}")

class MAEnvelopeStrategy(TradingStrategy):
    """Stratégie de trading MAEnvelope"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ma_envelope_period = kwargs.get("ma_envelope_period", None)
        self.ma_envelope_upper = kwargs.get("ma_envelope_upper", None)
        self.ma_envelope_lower = kwargs.get("ma_envelope_lower", None)

    def execute(self):
        """Exécute la stratégie de trading MAEnvelope"""
        print("Exécution de la stratégie MAEnvelope")
        print(f"MAEnvelope period: {self.ma_envelope_period}")
        print(f"MAEnvelope upper: {self.ma_envelope_upper}")
        print(f"MAEnvelope lower: {self.ma_envelope_lower}")

class BreakoutStrategy(TradingStrategy):
    """Stratégie de trading Breakout"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breakout_period = kwargs.get("breakout_period", None)
        self.breakout_upper = kwargs.get("breakout_upper", None)
        self.breakout_lower = kwargs.get("breakout_lower", None)

    def execute(self):
        """Exécute la stratégie de trading Breakout"""
        print("Exécution de la stratégie Breakout")
        print(f"Breakout period: {self.breakout_period}")
        print(f"Breakout upper: {self.breakout_upper}")
        print(f"Breakout lower: {self.breakout_lower}")

class IchimokuCloudStrategy(TradingStrategy):
    """Stratégie de trading IchimokuCloud"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ichimoku_cloud_period = kwargs.get("ichimoku_cloud_period", None)
        self.ichimoku_cloud_upper = kwargs.get("ichimoku_cloud_upper", None)
        self.ichimoku_cloud_lower = kwargs.get("ichimoku_cloud_lower", None)

    def execute(self):
        """Exécute la stratégie de trading IchimokuCloud"""
        print("Exécution de la stratégie IchimokuCloud")
        print(f"IchimokuCloud period: {self.ichimoku_cloud_period}")
        print(f"IchimokuCloud upper: {self.ichimoku_cloud_upper}")
        print(f"IchimokuCloud lower: {self.ichimoku_cloud_lower}")

class ATRStrategy(TradingStrategy):
    """Stratégie de trading ATR"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atr_period = kwargs.get("atr_period", None)
        self.atr_upper = kwargs.get("atr_upper", None)
        self.atr_lower = kwargs.get("atr_lower", None)

    def execute(self):
        """Exécute la stratégie de trading ATR"""
        print("Exécution de la stratégie ATR")
        print(f"ATR period: {self.atr_period}")
        print(f"ATR upper: {self.atr_upper}")
        print(f"ATR lower: {self.atr_lower}")

class MACDStrategy(TradingStrategy):
    """Stratégie de trading MACD"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.macd_period = kwargs.get("macd_period", None)
        self.macd_upper = kwargs.get("macd_upper", None)
        self.macd_lower = kwargs.get("macd_lower", None)

    def execute(self):
        """Exécute la stratégie de trading MACD"""
        print("Exécution de la stratégie MACD")
        print(f"MACD period: {self.macd_period}")
        print(f"MACD upper: {self.macd_upper}")
        print(f"MACD lower: {self.macd_lower}")