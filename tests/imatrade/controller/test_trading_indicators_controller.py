"""Module for testing trading indicators controller."""


def test_create_all_indicators(trading_indicators_controller):
    """Test hello world."""

    indicators = trading_indicators_controller.create_all_indicators()
    assert len(indicators) == 3
