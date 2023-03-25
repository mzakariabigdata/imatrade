"""
Contient les classes Builder (MACrossoverStrategyBuilder, RSIStrategyBuilder)
"""
from abc import ABC, abstractmethod
from .trading_strategy import (
    MACrossoverStrategy,
    RSIStrategy,
    BollingerBandsStrategy,
    StochasticOscillatorStrategy,
    ATRStrategy,
    MACDStrategy,
    IchimokuCloudStrategy,
    BreakoutStrategy,
    RSIDivergenceStrategy,
    MAEnvelopeStrategy
)


class TradingStrategyBuilder(ABC):
    @abstractmethod
    def build(self):
        pass

class MAEnvelopeStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.ma_period = None
        self.ma_type = None
        self.ma_distance = None

    def set_ma_period(self, ma_period):
        self.ma_period = ma_period
        return self

    def set_ma_type(self, ma_type):
        self.ma_type = ma_type
        return self

    def set_ma_distance(self, ma_distance):
        self.ma_distance = ma_distance
        return self

    def build(self, config):
        return MAEnvelopeStrategy(
            ma_period=config["ma_period"],
            ma_type=config["ma_type"],
            ma_distance=config["ma_distance"],
        )


class RSIDivergenceStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.short_rsi_period = None
        self.long_rsi_period = None
        self.signal_period = None

    def set_short_rsi_period(self, short_rsi_period):
        self.short_rsi_period = short_rsi_period
        return self

    def set_long_rsi_period(self, long_rsi_period):
        self.long_rsi_period = long_rsi_period
        return self

    def set_signal_period(self, signal_period):
        self.signal_period = signal_period
        return self

    def build(self, config):
        return RSIDivergenceStrategy(
            short_rsi_period=config["short_rsi_period"],
            long_rsi_period=config["long_rsi_period"],
            signal_period=config["signal_period"],
        )


class BollingerBandsStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.window = None
        self.num_std = None

    def set_window(self, window):
        self.window = window
        return self

    def set_num_std(self, num_std):
        self.num_std = num_std
        return self

    def build(self, config):
        return BollingerBandsStrategy(
            window=config["window"], num_std=config["num_std"]
        )


class ATRStrategyBuilder(TradingStrategyBuilder):
    def build(self, config):
        return ATRStrategy(window=config["window"])


class MACDStrategyBuilder(TradingStrategyBuilder):
    def build(self, config):
        return MACDStrategy(
            short_window=config["short_window"],
            long_window=config["long_window"],
            signal_window=config["signal_window"],
        )


class StochasticOscillatorStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.k_window = None
        self.d_window = None
        self.overbought = None
        self.oversold = None

    def set_k_window(self, k_window):
        self.k_window = k_window
        return self

    def set_d_window(self, d_window):
        self.d_window = d_window
        return self

    def set_overbought(self, overbought):
        self.overbought = overbought
        return self

    def set_oversold(self, oversold):
        self.oversold = oversold
        return self

    def build(self, config):
        return StochasticOscillatorStrategy(
            k_window=config["k_window"],
            d_window=config["d_window"],
            oversold=config["oversold"],
            overbought=config["overbought"],
        )


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
        return MACrossoverStrategy(
            short_window=config["short_window"], long_window=config["long_window"]
        )

class IchimokuCloudStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.conversion_line_period = None
        self.base_line_period = None
        self.lagging_span_periods = None
        self.displacement = None

    def set_conversion_line_period(self, conversion_line_period):
        self.conversion_line_period = conversion_line_period
        return self

    def set_base_line_period(self, base_line_period):
        self.base_line_period = base_line_period
        return self

    def set_lagging_span_periods(self, lagging_span_periods):
        self.lagging_span_periods = lagging_span_periods
        return self

    def set_displacement(self, displacement):
        self.displacement = displacement
        return self

    def build(self, config):
        return IchimokuCloudStrategy(
            conversion_line_period=config["conversion_line_period"],
            base_line_period=config["base_line_period"],
            lagging_span_periods=config["lagging_span_periods"],
            displacement=config["displacement"],
        )

class BreakoutStrategyBuilder(TradingStrategyBuilder):
    def __init__(self):
        self.lookback_window = None
        self.buy_margin = None
        self.sell_margin = None

    def set_lookback_window(self, lookback_window):
        self.lookback_window = lookback_window
        return self

    def set_buy_margin(self, buy_margin):
        self.buy_margin = buy_margin
        return self

    def set_sell_margin(self, sell_margin):
        self.sell_margin = sell_margin
        return self

    def build(self, config):
        return BreakoutStrategy(
            lookback_window=config["lookback_window"],
            buy_margin=config["buy_margin"],
            sell_margin=config["sell_margin"],
        )


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
        return RSIStrategy(
            rsi_period=config["rsi_period"],
            oversold=config["oversold"],
            overbought=config["overbought"],
        )
