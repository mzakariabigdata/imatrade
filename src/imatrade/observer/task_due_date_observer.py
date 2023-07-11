"""Module définissant l'observateur de tâches qui affiche les dates d'échéance des tâches."""
from src.imatrade.observer.task_observer import TaskObserver

# from src.imatrade.model import TaskV2


class TaskDueDateObserver(TaskObserver):  # pylint: disable=too-few-public-methods
    """
    Observateur de tâches qui affiche les dates d'échéance des tâches.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def update(self, task):
        self.strategy.execute(task)
