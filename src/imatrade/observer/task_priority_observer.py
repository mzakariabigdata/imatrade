from imatrade.observer.task_observer import TaskObserver


class TaskPriorityObserver(TaskObserver):
    """
    Observateur de tâches qui suit les priorités des tâches.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def update(self, task):
        self.strategy.execute(task)
