"""
Module for building trading backtests.
"""


from imobject import ObjDict
from src.imatrade.model.trading_backtest import TradingBacktest
from src.imatrade.utils.config import APPLICATION


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
            strategies = {}
            for strategy in list(backtest_config.strategies):
                strategy_obj = APPLICATION.trading_strategy_controller.get_strategy(
                    strategy.get("name")
                )
                strategies[strategy.get("name")] = strategy_obj
            backtest_config.strategies = strategies
            backtest = TradingBacktest(**backtest_config)
            backtests.append(backtest)
        return backtests
