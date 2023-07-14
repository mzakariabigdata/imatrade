"""Module for testing trading backtests controller."""


def test_create_all_backtests(trading_backtest_controller):
    """Test hello world."""

    backtests = trading_backtest_controller.create_all_backtests()
    assert len(backtests) == 2
