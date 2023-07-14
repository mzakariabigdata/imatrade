"""
Module for building trading backtests.
"""


from imobject import ObjDict
from src.imatrade.model.trading_backtest import TradingBacktest
from src.imatrade.model.trading_strategy_builder import TradingStrategyBuilder


class TradingBacktestBuilder:
    """Class for trading backtests builder."""

    def build(self, backtests_config):
        """Method to build a trading backtest."""
        backtests = self.build_backtests(backtests_config)
        return backtests

    def build_backtests(self, backtests_config):
        """Method to build trading backtests."""
        backtests = []
        for backtest_config in backtests_config:
            backtest_config = ObjDict(backtest_config)
            strategies = TradingStrategyBuilder().build_strategies(
                backtest_config.strategies
            )
            backtest_config.strategies = strategies
            backtest = TradingBacktest(**backtest_config)
            backtests.append(backtest)
        return backtests
