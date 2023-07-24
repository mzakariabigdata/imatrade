"""
Contient la classe TradingStrategyFactory pour créer des stratégies
"""
import importlib
from src.imatrade import Singleton


class TradingStrategyFactory(metaclass=Singleton):
    """Classe pour créer des stratégies de trading"""

    def __init__(self, strategies_composer):
        self._builder = None
        self.strategies = []
        self.strategies_composer = strategies_composer

    def load_builder(self):
        """Charger le builder de stratégie de trading"""
        module = importlib.import_module("src.imatrade.model.trading_strategy_builder")
        builder_class = getattr(module, "TradingStrategyBuilder")
        builder_instance = builder_class()
        self._builder = builder_instance
        self.load_strategies()

    def load_strategies(self):
        """Charger les stratégies de trading"""
        for strategy in self.strategies_composer.strategies:
            self.strategies.append(strategy["name"])

    def get_registered_strategy_names(self):
        """Obtenir les noms des stratégies de trading enregistrées"""
        return self.strategies

    def create_strategy(self, strategy_name: str):
        """Créer une stratégie de trading

        Args:
            strategy_name (str):  Nom de la stratégie

        Raises:
            ValueError:  Si le nom de la stratégie n'est pas valide

        Returns:
            _type_:  Stratégie de trading
        """
        if not self._builder:
            raise ValueError("Builder not loaded")
        if strategy_name not in self.strategies:
            raise ValueError(f"Invalid strategy name: {strategy_name}")
        strategy_config = self.strategies_composer.strategies.where(
            name__eq=strategy_name
        )
        return self._builder.build(strategy_config.find_by(name=strategy_name))
