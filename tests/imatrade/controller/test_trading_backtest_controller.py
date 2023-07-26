"""Module for testing trading backtests controller."""
from src.imatrade.model.trading_backtest import TradingBacktest
from src.imatrade.utils.config import APPLICATION


def test_create_all_backtests(trading_backtest_controller, trading_strategy_controller):
    """Test hello world."""

    APPLICATION.trading_strategy_controller = trading_strategy_controller

    backtests = trading_backtest_controller.create_all_backtests()
    assert isinstance(backtests.get("dolar_euro_macd_1_for_test"), TradingBacktest)
    assert len(backtests) == 2
