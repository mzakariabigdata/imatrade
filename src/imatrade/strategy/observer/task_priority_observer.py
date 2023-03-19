from imatrade.strategy.observer.observer_strategy import ObserverStrategy


class TaskPriorityStrategy(ObserverStrategy):
    """
    Stratégie d'observateur qui met à jour le comptage des priorités de tâches.
    """

    def __init__(self):
        self.priority_counts = {}

    def execute(self, task):
        priority_level = task.priority_level
        if priority_level not in self.priority_counts:
            self.priority_counts[priority_level] = 0
        self.priority_counts[priority_level] += 1
        print(f"Nombre de tâches par niveau de priorité : {self.priority_counts}")
