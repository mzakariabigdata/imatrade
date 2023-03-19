from imatrade.model.task import Task


class TaskBuilder:
    """
    Constructeur de tâches pour créer des instances de tâches.
    """

    def __init__(self):
        self.title = ""
        self.priority = 1

    def set_title(self, title):
        self.title = title
        return self

    def set_priority(self, priority):
        self.priority = priority
        return self

    def build(self):
        return Task(self.title, self.priority)
