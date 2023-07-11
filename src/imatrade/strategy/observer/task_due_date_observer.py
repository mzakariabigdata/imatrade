"""module définissant la stratégie d'observateur qui affiche la date d'échéance de la tâche."""

from src.imatrade.strategy.observer.observer_strategy import ObserverStrategy


class TaskDueDateStrategy(ObserverStrategy):  # pylint: disable=too-few-public-methods
    """
    Stratégie d'observateur qui affiche la date d'échéance de la tâche.
    """

    def execute(self, task):
        if hasattr(task, "due_date"):
            due_date = task.due_date
            print(f"La date d'échéance de la tâche '{task.title}' est {due_date}.")
        else:
            print(f"La tâche '{task.title}' n'a pas de date d'échéance.")
