"""
Module pour les builders d'indicateurs de trading.
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
        """Méthode pour construire un indicateur de trading"""
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
            module = importlib.import_module("src.imatrade.model.trading_indicator")
            # get all classes from module
            classes = [x for x in dir(module) if x.endswith("Indicator")]
            # get class from classes the name of the indicator class
            class_name = [
                x for x in classes if indicator_config.name + "Indicator" == x
            ]
            # check if class_name is empty or has more than one element
            if not class_name or len(class_name) > 1:
                raise ValueError(
                    f"Invalid indicator name: {indicator_config.name} \n"
                    + "valid indicator names are: \n"
                    + f"{[x.replace('Indicator', '') for x in classes]}"
                )
            indicator_class = getattr(module, f"{class_name[0]}")
            indicator = indicator_class(**indicator_config)
            indicators.append(indicator)
        return indicators
