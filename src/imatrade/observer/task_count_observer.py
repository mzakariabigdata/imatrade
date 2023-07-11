"""Module définissant la classe TaskCountObserver."""
from src.imatrade.observer.task_observer import TaskObserver


class TaskCountObserver(TaskObserver):  # pylint: disable=too-few-public-methods
    """
    Observateur de tâches qui suit le nombre total de tâches.
    """

    def __init__(self, strategy):
        # self.task_count = 0
        self.strategy = strategy

    def update(self, task):
        # self.task_count += 1
        # print(f"Nombre total de tâches : {self.task_count}")

        self.strategy.execute(task)
