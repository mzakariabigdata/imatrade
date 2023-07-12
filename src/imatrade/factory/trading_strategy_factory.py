"""
Contient la classe TradingStrategyFactory pour créer des stratégies
"""
import importlib
from src.imatrade.utils.config import APPLICATION
from src.imatrade import Singleton


class TradingStrategyFactory(metaclass=Singleton):
    """Classe pour créer des stratégies de trading"""

    def __init__(self):
        self._builder = None
        self.strategies = []
        self.strategies_composer = APPLICATION.strategies_config.strategies_composer

    def load_builder(self):
        """Charger le builder de stratégie de trading"""
        module = importlib.import_module(
            f"imatrade.model.{self.strategies_composer.builder.module_path}"
        )
        builder_class = getattr(
            module, f"{self.strategies_composer.builder.class_name}"
        )
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
        strategy_config = self.strategies_composer.strategies.where(name=strategy_name)
        print(f"strategy_config for {strategy_name}", strategy_config)
        return self._builder.build(strategy_config.find_by(name=strategy_name))
