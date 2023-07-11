"""Module pour les observateurs de tâches."""
from abc import ABC, abstractmethod


class TaskObserver(ABC):  # pylint: disable=too-few-public-methods
    """
    Classe de base abstraite pour les observateurs de tâches.
    """

    @abstractmethod
    def update(self, task):
        """Méthode abstraite pour mettre à jour l'observateur."""
