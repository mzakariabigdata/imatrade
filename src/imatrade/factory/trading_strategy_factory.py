"""
Contient la classe TradingStrategyFactory pour créer des stratégies
"""
from imatrade.model import RSIStrategyBuilder, MACrossoverStrategyBuilder
from imatrade.utils.config import strategies_config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TradingStrategyFactory(metaclass=Singleton):
    def __init__(self):
        self._builders = {}

    # def create_all_strategy(self):
    #     for strategy_name, strategy_config in strategies_config.items():
    #         if strategy_name == "MA_Crossover":
    #             builder = MACrossoverStrategyBuilder()
    #         elif strategy_name == "RSI":
    #             builder = RSIStrategyBuilder()
    #         else:
    #             continue  # Ignore any other strategy types
    #         self.register_builder(strategy_name, builder)

    def get_registered_strategy_names(self):
        return list(self._builders.keys())

    def register_builder(self, strategy_name, builder):
        self._builders[strategy_name] = builder

    def create_strategy(self, strategy_name):
        builder = self._builders.get(strategy_name)
        if not builder:
            raise ValueError(f"Invalid strategy name: {strategy_name}")
        strategy_config = strategies_config.get(strategy_name)
        return builder.build(strategy_config)
