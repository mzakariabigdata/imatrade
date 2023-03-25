from abc import ABC, abstractmethod


class TaskInterface(ABC):
    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def display(self):
        pass


class Task(TaskInterface):
    """
    Classe de base abstraite pour les tâches.
    """

    def __init__(self, title, priority_level):
        self.title = title
        self.priority_level = priority_level

    def __str__(self):
        return f"{self.title} (Priorité: {self.priority_level})"

    def perform_task(self):
        print(f"Execute task : {self.title}")


class TaskV1(Task):
    """
    Implémentation de la version 1 de la tâche avec des attributs de base.
    """

    def __init__(self, title, priority_level, description):
        super().__init__(title, priority_level)
        self.description = description

    def get_priority_level(self):
        return self.priority_level

    def set_priority_level(self, priority_level):
        self.priority_level = priority_level

    def __str__(self):
        return f"{self.title} (Priorité: {self.priority_level}, description: {self.description})"

    # Implémentation de la méthode perform de l'interface TaskInterface
    def perform(self):
        # Ici, vous pouvez ajouter le code pour effectuer la tâche
        print(f"Effectuer la tâche V1 : {self.title}")

    # Implémentation de la méthode display de l'interface TaskInterface
    def display(self):
        # Ici, vous pouvez ajouter le code pour afficher la tâche
        print(f"Tâche V1 : {self.title} ({self.priority_level})")


class TaskV2(Task):
    """
    Implémentation de la version 2 de la tâche avec des attributs supplémentaires.
    """

    def __init__(self, title, description, due_date):
        super().__init__(title, description)
        self.due_date = due_date

    def get_due_date(self):
        return self.due_date

    def set_due_date(self, due_date):
        self.due_date = due_date

    # Implémentation de la méthode perform de l'interface TaskInterface
    def perform(self):
        # Ici, vous pouvez ajouter le code pour effectuer la tâche
        print(f"Effectuer la tâche V1 : {self.title}")

    # Implémentation de la méthode display de l'interface TaskInterface
    def display(self):
        # Ici, vous pouvez ajouter le code pour afficher la tâche
        print(f"Tâche V1 : {self.title} ({self.due_date})")
