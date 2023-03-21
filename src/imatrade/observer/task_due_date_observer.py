from imatrade.observer.task_observer import TaskObserver
from imatrade.model import TaskV2


class TaskDueDateObserver(TaskObserver):
    """
    Observateur de tâches qui affiche les dates d'échéance des tâches.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def update(self, task):
        self.strategy.execute(task)
