"""
Contient les classes Stategy
"""

from abc import ABC, abstractmethod


class TradingStrategy(ABC):  # pylint: disable=too-few-public-methods
    """Classe abstraite pour les stratégies de trading."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")

    @abstractmethod
    def execute(self):
        """Méthode abstraite pour exécuter la stratégie."""
