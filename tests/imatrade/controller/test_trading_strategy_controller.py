"""Module de test pour le controller de stratégies de trading."""


def test_create_all_strategies(trading_strategy_controller):
    """Test hello world."""
    strategies = trading_strategy_controller.create_all_strategies()
    assert len(strategies) == 5
