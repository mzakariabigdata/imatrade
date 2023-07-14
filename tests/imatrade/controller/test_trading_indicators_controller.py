"""Module for testing trading indicators controller."""

from src.imatrade.model.trading_indicator import TradingIndicator


def test_create_all_indicators(trading_indicators_controller):
    """Test hello world."""

    indicators = trading_indicators_controller.create_all_indicators()
    assert isinstance(indicators.get("MACD"), TradingIndicator)
    assert len(indicators) == 3
