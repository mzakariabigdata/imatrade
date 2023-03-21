# controller/trading_strategy_controller.py

from imatrade.model.trading_strategy import TradingStrategy
from imatrade.view.trading_strategy_view import TradingStrategyView

class TradingStrategyController:
    def __init__(self, strategy_factory):
        self.strategy_factory = strategy_factory

    def create_strategy(self, strategy_type, **kwargs):
        strategy = self.strategy_factory.create_strategy(strategy_type, **kwargs)
        return strategy

    def display_strategy(self, strategy):
        TradingStrategyView.display_strategy(strategy)

    def display_data(self, data):
        TradingStrategyView.display_data(data)

    def display_signals(self, signals):
        TradingStrategyView.display_signals(signals)

    def execute_strategy(self, strategy, market_data):
        strategy.prepare_data(market_data)
        signals = strategy.generate_signals()
        self.display_signals(signals)
        return signals

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass