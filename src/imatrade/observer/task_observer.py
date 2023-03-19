from abc import ABC, abstractmethod


class TaskObserver(ABC):
    """
    Classe de base abstraite pour les observateurs de tâches.
    """

    @abstractmethod
    def update(self, task):
        pass
