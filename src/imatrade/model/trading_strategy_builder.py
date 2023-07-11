"""
Contient les classes Builder (MACrossoverStrategyBuilder, RSIStrategyBuilder)
"""
from abc import ABC, abstractmethod
import importlib
from imobject import ObjDict

# q: pourquoi on a besoin de ABC?
# r: pour forcer les classes filles à implémenter les méthodes abstraites


# q: c'est quoi le but de cette classe?
# r: c'est une classe abstraite qui va servir de base pour les classes filles
class ABSTradingStrategyBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Classe abstraite pour les builders de stratégies de trading"""

    @abstractmethod
    def build(self, strategy_config):
        """Méthode abstraite pour construire une stratégie de trading"""


class ABSTradingIndicatorBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Classe abstraite pour les builders d'indicateurs de trading"""

    @abstractmethod
    def build(self, indicators_config):
        """Méthode abstraite pour construire un indicateur de trading"""


class TradingStrategyBuilder(
    ABSTradingStrategyBuilder
):  # pylint: disable=too-few-public-methods
    """Builder pour les stratégies de trading"""

    def build(self, strategy_config):
        strategy_config = ObjDict(strategy_config)
        # module = importlib.import_module(
        #     f"imatrade.model.{strategy_config.module_path}"
        # )
        # print("indicators", strategy_config.indicators)
        indicators = TradingIndicatorBuilder().build(strategy_config.indicators)
        # strategy_class = getattr(module, f"{strategy_config.class_name}")
        # return strategy_class(**strategy_config)
        return indicators[0]


class TradingIndicatorBuilder(
    ABSTradingIndicatorBuilder
):  # pylint: disable=too-few-public-methods
    """Builder pour les indicateurs de trading"""

    def build(self, indicators_config):
        # indicators_config = ObjDict(indicators_config)
        indicators = []
        for indicator_config in indicators_config:
            indicator_config = ObjDict(indicator_config)
            module = importlib.import_module(
                f"imatrade.model.{indicator_config.module_path}"
            )
            indicator_class = getattr(module, f"{indicator_config.class_name}")
            indicator = indicator_class(**indicator_config)
            indicators.append(indicator)
        print("indicators", indicators)
        return indicators
