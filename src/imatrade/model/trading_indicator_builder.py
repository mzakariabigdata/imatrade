"""
Contient les classes indicateur de trading builder
"""

from abc import ABC, abstractmethod
import importlib
from imobject import ObjDict


class ABSTradingIndicatorBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Classe abstraite pour les builders d'indicateurs de trading"""

    @abstractmethod
    def build(self, indicators_config):
        """Méthode abstraite pour construire un indicateur de trading"""


class TradingIndicatorBuilder(
    ABSTradingIndicatorBuilder
):  # pylint: disable=too-few-public-methods
    """Builder pour les stratégies de trading"""

    def build(self, indicators_config):
        # indicator_config = ObjDict(indicator_config[0])
        indicators = TradingIndicatorsBuilder().build(indicators_config)
        return indicators


class TradingIndicatorsBuilder(
    ABSTradingIndicatorBuilder
):  # pylint: disable=too-few-public-methods
    """Builder pour les indicateurs de trading"""

    def build(self, indicators_config):
        # indicators_config = ObjDict(indicators_config)
        indicators = []
        for indicator_config in indicators_config:
            indicator_config = ObjDict(indicator_config)
            module = importlib.import_module(
                f"src.imatrade.model.{indicator_config.module_path}"
            )
            indicator_class = getattr(module, f"{indicator_config.class_name}")
            indicator = indicator_class(**indicator_config)
            indicators.append(indicator)
        return indicators
