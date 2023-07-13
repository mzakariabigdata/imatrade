"""
Contient la classe TradingIndicatorsFactory pour créer des indicators
"""

import importlib
from src.imatrade.utils.config import APPLICATION
from src.imatrade import Singleton


class TradingIndicatorsFactory(metaclass=Singleton):
    """Classe pour créer des indicators de trading"""

    def __init__(self):
        self._builder = None
        self.indicators = []
        self.indicators_composer = APPLICATION.indicators_config.indicators_composer

    def load_builder(self):
        """Charger le builder d'indicators de trading"""
        module = importlib.import_module(
            f"imatrade.model.{self.indicators_composer.builder.module_path}"
        )
        builder_class = getattr(
            module, f"{self.indicators_composer.builder.class_name}"
        )
        builder_instance = builder_class()
        self._builder = builder_instance
        self.load_indicators()

    def load_indicators(self):
        """Charger les indicators de trading"""
        for indicator in self.indicators_composer.indicators:
            self.indicators.append(indicator["name"])

    def get_registered_indicator_names(self):
        """Obtenir les noms des indicators de trading enregistrés"""
        return self.indicators

    def create_indicator(self, indicator_name: str):
        """Créer un indicator de trading

        Args:
            indicator_name (str):  Nom de l'indicator

        Raises:
            ValueError:  Si le nom de l'indicator n'est pas valide

        Returns:
            _type_:  Indicator de trading
        """
        if not self._builder:
            raise ValueError("Builder not loaded")
        if indicator_name not in self.indicators:
            raise ValueError(f"Invalid indicator name: {indicator_name}")
        indicator_config = self.indicators_composer.indicators.where(
            name=indicator_name
        )
        return self._builder.build(indicator_config)[0]
