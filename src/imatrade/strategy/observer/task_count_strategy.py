"""Cas d'utilisation de la stratégie d'observateur pour compter les tâches."""

from src.imatrade.strategy.observer.observer_strategy import ObserverStrategy


class TaskCountStrategy(ObserverStrategy):  # pylint: disable=too-few-public-methods
    """
    Stratégie d'observateur qui met à jour le comptage des tâches.
    """

    def __init__(self):
        self.task_count = 0

    def execute(self, task):
        """Met à jour le comptage des tâches"""
        self.task_count += 1
        print(f"Nombre total de tâches: {self.task_count}")
