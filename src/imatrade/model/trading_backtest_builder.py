"""
Module for building trading backtests.
"""


from abc import ABC, abstractmethod
import importlib
from imobject import ObjDict


class ABSTradingBacktestBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class for trading backtests builder."""

    @abstractmethod
    def build(self, backtests_config):
        """Abstract method to build a trading backtest."""


class TradingBacktestBuilder(
    ABSTradingBacktestBuilder
):  # pylint: disable=too-few-public-methods
    """Class for trading backtests builder."""

    def build(self, backtests_config):
        """Method to build a trading backtest."""
        backtests = TradingBacktestsBuilder().build(backtests_config)
        return backtests


class TradingBacktestsBuilder(
    ABSTradingBacktestBuilder
):  # pylint: disable=too-few-public-methods
    """Class for trading backtests builder."""

    def build(self, backtests_config):
        """Method to build trading backtests."""
        backtests = []
        for backtest_config in backtests_config:
            backtest_config = ObjDict(backtest_config)
            module = importlib.import_module(
                f"src.imatrade.model.{backtest_config.module_path}"
            )
            backtest_class = getattr(module, f"{backtest_config.class_name}")
            backtest = backtest_class(**backtest_config)
            backtests.append(backtest)
        return backtests
