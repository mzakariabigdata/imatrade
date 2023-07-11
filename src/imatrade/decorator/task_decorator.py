"""Ce module contient les classes de base pour les décorateurs de tâches."""
from src.imatrade.model.task import TaskInterface


class TaskDecorator(TaskInterface):
    """Classe de base abstraite pour les décorateurs de tâches."""

    def __init__(self, task: TaskInterface):
        self._task = task

    def perform(self):
        """Méthode pour effectuer la tâche."""
        self._task.perform()

    def display(self):
        """Méthode pour afficher la tâche."""
        self._task.display()


# class TaskDecorator(Task, ABC):
#     """
#     Classe de base abstraite pour les décorateurs de tâches.
#     """

#     def __init__(self, task):
#         self._task = task

#     @abstractmethod
#     def perform_task(self):
#         """Méthode abstraite pour effectuer la tâche."""


class UrgentTaskDecorator(TaskDecorator):
    """Classe de décorateur de tâches urgentes."""

    def perform(self):
        """Méthode pour effectuer la tâche."""
        print("Attention, tâche urgente !")
        self._task.perform()

    def display(self):
        """Méthode pour afficher la tâche."""
        print("Urgent : ", end="")
        self._task.display()


class TaskWithLogging(TaskDecorator):
    """
    Décorateur de tâches qui ajoute des fonctionnalités de journalisation.
    """

    def perform_task(self):
        """Méthode pour effectuer la tâche."""
        print(f"Task started: {self._task.__class__.__name__}")
        result = self._task.perform_task()
        print(f"Task finished: {self._task.__class__.__name__}")
        return result

    def __str__(self):
        return str(self._task)

    def __getattr__(self, attr):
        return getattr(self._task, attr)

    def perform(self):
        """Méthode pour effectuer la tâche."""
        self._task.perform()

    def display(self):
        """Méthode pour afficher la tâche."""
        self._task.display()
