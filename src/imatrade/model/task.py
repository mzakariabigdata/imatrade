class Task:
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
