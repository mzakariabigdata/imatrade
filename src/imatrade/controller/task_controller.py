"""Module contenant le contrôleur de tâches"""
from src.imatrade.view.task_view import TaskView
from src.imatrade.observer.task_observer import TaskObserver
from src.imatrade.factory.task_factory import ExtendedTaskFactory


class SingletonTaskObserver(TaskObserver):
    """
    Classe d'observateur de tâches avec un comportement Singleton.
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
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
        """methode qui ajoute une tâche à la liste des tâches"""
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
        """methode qui affiche les tâches"""
        sorted_tasks = self.sorting_strategy.sort_tasks(self.tasks)
        TaskView.display_tasks(sorted_tasks)

    def perform_tasks(self):
        """methode qui effectue les tâches"""
        TaskView.perform_tasks(self.tasks)

    def update(self, task):
        """methode qui met à jour la liste des tâches"""
        print(f"Nouvelle tâche ajoutée : {task}")

    def notify_observers(self, task):
        """methode qui notifie les observateurs"""
        for observer in self.observers:
            observer.update(task)
