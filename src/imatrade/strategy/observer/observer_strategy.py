from abc import ABC, abstractmethod


class ObserverStrategy(ABC):
    """
    Classe de base abstraite pour les stratégies d'observateur.
    """

    @abstractmethod
    def execute(self, task):
        pass
