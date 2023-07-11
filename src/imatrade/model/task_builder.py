"""Module contenant le constructeur de tâches."""
from .task import TaskV1


class TaskBuilder:
    """
    Constructeur de tâches pour créer des instances de tâches.
    """

    def __init__(self):
        self.title = ""
        self.priority = 1
        self.description = ""

    def set_title(self, title):
        """Méthode pour définir le titre de la tâche."""
        self.title = title
        return self

    def set_priority(self, priority):
        """Méthode pour définir la priorité de la tâche."""
        self.priority = priority
        return self

    def set_description(self, description):
        """Méthode pour définir la description de la tâche."""
        self.description = description
        return self

    def build(self):
        """Méthode pour construire une tâche."""
        return TaskV1(self.title, self.priority, self.description)
