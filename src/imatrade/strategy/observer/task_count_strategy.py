from imatrade.strategy.observer.observer_strategy import ObserverStrategy


class TaskCountStrategy(ObserverStrategy):
    """
    Stratégie d'observateur qui met à jour le comptage des tâches.
    """

    def __init__(self):
        self.task_count = 0

    def execute(self, task):
        self.task_count += 1
        print(f"Nombre total de tâches: {self.task_count}")
