"""
Contient la classe TradingStrategyFactory pour créer des stratégies
"""
from imatrade.model import RSIStrategyBuilder, MACrossoverStrategyBuilder 

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class TradingStrategyFactory(metaclass=Singleton):
    def __init__(self):
        self._builders = {}

    def register_builder(self, strategy_type, builder):
        self._builders[strategy_type] = builder

    @staticmethod
    def create_strategy(strategy_type, **kwargs):
        if strategy_type == "MA_Crossover":
            builder = MACrossoverStrategyBuilder()
            return builder.set_short_window(kwargs["short_window"]).set_long_window(kwargs["long_window"]).build()
        elif strategy_type == "RSI":
            builder = RSIStrategyBuilder()
            return builder.set_rsi_period(kwargs["rsi_period"]).set_overbought(kwargs["overbought"]).set_oversold(kwargs["oversold"]).build()
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")