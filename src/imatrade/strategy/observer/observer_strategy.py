"""Module pour les stratégies d'observateur"""
from abc import ABC, abstractmethod


class ObserverStrategy(ABC):  # pylint: disable=too-few-public-methods
    """
    Classe de base abstraite pour les stratégies d'observateur.
    """

    @abstractmethod
    def execute(self, task):
        """Methode abstraite pour exécuter la stratégie."""
