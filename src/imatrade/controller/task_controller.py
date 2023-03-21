from imatrade.model import Task
from imatrade.model import TaskBuilder
from imatrade.view.task_view import TaskView
from imatrade.observer.task_observer import TaskObserver
from imatrade.factory.task_factory import TaskFactory, ExtendedTaskFactory


class SingletonTaskObserver(TaskObserver):
    """
    Classe d'observateur de tâches avec un comportement Singleton.
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonTaskObserver, cls).__new__(cls)
        return cls._instances[cls]


class TaskController(SingletonTaskObserver):
    """
    Contrôleur de tâches qui gère l'ajout, l'affichage et l'exécution de tâches.
    """

    def __init__(self, sorting_strategy, observers=None):
        self.tasks = []
        self.sorting_strategy = sorting_strategy
        self.observers = observers if observers else []

    def add_task(self):
        title = TaskView.get_task_title()
        priority = TaskView.get_task_priority()
        description = TaskView.get_task_description()

        # task = TaskFactory.create_task(title, priority)
        task_factory = ExtendedTaskFactory()
        task = task_factory.create_task("v1", title, priority, description)
        self.tasks.append(task)

        self.update(task)
        self.notify_observers(task)

    def display_tasks(self):
        sorted_tasks = self.sorting_strategy.sort_tasks(self.tasks)
        TaskView.display_tasks(sorted_tasks)

    def perform_tasks(self):
        TaskView.perform_tasks(self.tasks)

    def update(self, task):
        print(f"Nouvelle tâche ajoutée : {task}")

    def notify_observers(self, task):
        for observer in self.observers:
            observer.update(task)
