"""
Contient les classes Builder (MACrossoverStrategyBuilder, RSIStrategyBuilder)
"""
import importlib
from imobject import ObjDict
from abc import ABC, abstractmethod

# q: pourquoi on a besoin de ABC?
# r: pour forcer les classes filles à implémenter les méthodes abstraites


# q: c'est quoi le but de cette classe?
# r: c'est une classe abstraite qui va servir de base pour les classes filles
class ABSTradingStrategyBuilder(ABC):
    @abstractmethod
    def build(self):
        pass


class TradingStrategyBuilder(ABSTradingStrategyBuilder):
    def build(self, strategy_config):
        strategy_config = ObjDict(strategy_config)
        module = importlib.import_module(
            f"imatrade.model.{strategy_config.module_path}"
        )
        strategy_class = getattr(module, f"{strategy_config.class_name}")
        return strategy_class(**strategy_config)
