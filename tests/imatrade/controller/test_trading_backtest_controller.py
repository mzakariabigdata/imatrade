"""Module for testing trading backtests controller."""
from src.imatrade.model.trading_backtest import TradingBacktest


def test_create_all_backtests(trading_backtest_controller):
    """Test hello world."""

    backtests = trading_backtest_controller.create_all_backtests()
    assert isinstance(backtests.get("dolar_euro_macd_1_for_test"), TradingBacktest)
    assert len(backtests) == 2
