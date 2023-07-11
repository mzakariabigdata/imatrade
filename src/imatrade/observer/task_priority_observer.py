"""Module des observateurs de tâches qui suivent les priorités des tâches."""

from src.imatrade.observer.task_observer import TaskObserver


class TaskPriorityObserver(TaskObserver):  # pylint: disable=too-few-public-methods
    """
    Observateur de tâches qui suit les priorités des tâches.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def update(self, task):
        """Met à jour le comptage des priorités des tâches."""
        self.strategy.execute(task)
