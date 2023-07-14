"""Module de test pour le controller de stratégies de trading."""

from src.imatrade.model.trading_strategy import TradingStrategy


def test_create_all_strategies(trading_strategy_controller):
    """Test hello world."""

    strategies = trading_strategy_controller.create_all_strategies()
    assert isinstance(strategies.get("ATR_strategy_for_test"), TradingStrategy)
    assert len(strategies) == 5
