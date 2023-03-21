# controller/trading_strategy_controller.py

from imatrade.model.trading_strategy import TradingStrategy
from imatrade.view.trading_strategy_view import TradingStrategyView

class TradingStrategyController:
    def __init__(self, strategy_factory):
        self.strategy_factory = strategy_factory
        self.strategies = {}  # Stocker les stratégies créées

    def create_all_strategies(self):
        for strategy_name in self.strategy_factory.get_registered_strategy_names():
            strategy = self.strategy_factory.create_strategy(strategy_name)
            self.add_strategy(strategy_name, strategy)
        return self.strategies
    
    def create_strategy(self, strategy_type):
        strategy_name, strategy = self.strategy_factory.create_strategy(strategy_type)
        self.add_strategy(strategy_name, strategy)  # Ajouter la stratégie au dictionnaire
        return strategy

    def add_strategy(self, strategy_name, strategy):
        self.strategies[strategy_name] = strategy

    def get_strategy(self, strategy_name):
        return self.strategies.get(strategy_name)
    
    def remove_strategy(self, strategy_name):
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]

    def display_all_strategies(self):
        for strategy_name, strategy in self.strategies.items():
            print(f"\nStrategy name: {strategy_name}")
            TradingStrategyView.display_strategy(strategy)

    def display_strategy(self, strategy_name):
        strategy = self.get_strategy(strategy_name)
        TradingStrategyView.display_strategy(strategy)

    def display_data(self, data):
        TradingStrategyView.display_data(data)

    def display_signals(self, signals):
        TradingStrategyView.display_signals(signals)

    def execute_strategy(self, strategy_name, market_data):
        strategy = self.get_strategy(strategy_name)
        strategy.prepare_data(market_data)
        signals = strategy.generate_signals()
        self.display_signals(signals)
        return signals

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass