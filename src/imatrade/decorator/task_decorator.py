from abc import ABC, abstractmethod
from imatrade.model import Task


class TaskDecorator(Task, ABC):
    """
    Classe de base abstraite pour les décorateurs de tâches.
    """

    def __init__(self, task):
        self._task = task

    @abstractmethod
    def perform_task(self):
        pass


class TaskWithLogging(TaskDecorator):
    """
    Décorateur de tâches qui ajoute des fonctionnalités de journalisation.
    """

    def perform_task(self):
        print(f"Task started: {self._task.__class__.__name__}")
        result = self._task.perform_task()
        print(f"Task finished: {self._task.__class__.__name__}")
        return result

    def __str__(self):
        return str(self._task)

    def __getattr__(self, attr):
        return getattr(self._task, attr)
