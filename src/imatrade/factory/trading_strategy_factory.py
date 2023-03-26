"""
Contient la classe TradingStrategyFactory pour créer des stratégies
"""
from imatrade.model.trading_strategy_builder import TradingStrategyBuilder, MACrossoverStrategyBuilder
import importlib
from typing import List
from imatrade.utils.config import APPLICATION

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

    def load_builders(self):
        for strategy in APPLICATION.strategies_config.strategies:
            module = importlib.import_module(f"imatrade.model.{strategy['module_path']}_builder")
            # strategy_class = getattr(module, strategy['class_name'])
            builder_class = getattr(module, f"{strategy['class_name']}Builder")
            builder_instance = builder_class()
            
            self.register_builder(strategy['name'], builder_instance)

    def get_registered_strategy_names(self):
        return list(self._builders.keys())

    def register_builder(self, strategy_name, builder):
        self._builders[strategy_name] = builder

    def create_strategy(self, strategy_name):
        builder = self._builders.get(strategy_name)
        if not builder:
            raise ValueError(f"Invalid strategy name: {strategy_name}")
        strategy_config = APPLICATION.strategies_config.strategies.where(name=strategy_name)
        return builder.build(strategy_config.find_by(name=strategy_name))
