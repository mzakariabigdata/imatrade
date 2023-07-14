"""
Module pour les builders de stratégies de trading.
"""
from imobject import ObjDict
from src.imatrade.model.trading_indicator_builder import TradingIndicatorsBuilder
from src.imatrade.model.trading_strategy import TradingStrategy


class TradingStrategyBuilder:
    """Builder pour les stratégies de trading"""

    def build_strategies(self, strategies_config):
        """Méthode pour construire des stratégies de trading"""
        strategies = []
        for strategy_config in strategies_config:
            strategy_config = ObjDict(strategy_config)
            strategy = self.build(strategy_config)
            strategies.append(strategy)
        return strategies

    def build(self, strategy_config):
        """Méthode pour construire une stratégie de trading"""
        strategy_config = ObjDict(strategy_config)

        indicators = TradingIndicatorsBuilder().build(strategy_config.indicators)

        strategy = TradingStrategy(
            name=strategy_config.name,
            indicators=indicators,
            description=strategy_config.description,
        )

        return strategy
