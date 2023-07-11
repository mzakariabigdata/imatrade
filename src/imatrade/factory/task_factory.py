"""Module pour la création de tâches."""
from src.imatrade.model import TaskV1, TaskV2
from src.imatrade.decorator.task_decorator import TaskWithLogging

# q: pourquoi on a besoin de ABC?
# r: pour forcer les classes filles à implémenter les méthodes abstraites


# q: c'est quoi le but de cette classe?
# r: c'est une classe abstraite qui va servir de base pour les classes filles


class TaskV1Factory:  # pylint: disable=too-few-public-methods
    """
    Factory pour créer des instances de tâches de version 1.
    """

    def create_task(self, title, priority_level, description):
        """Méthode pour créer une tâche."""
        return TaskV1(title, priority_level, description)


class TaskV2Factory:  # pylint: disable=too-few-public-methods
    """
    Factory pour créer des instances de tâches de version 2.
    """

    def create_task(self, title, description, due_date):
        """Méthode pour créer une tâche."""
        return TaskV2(title, description, due_date)


class ExtendedTaskFactory:  # pylint: disable=too-few-public-methods
    """
    Factory étendue pour créer des instances de tâches en fonction de la version.
    """

    @staticmethod
    def create_task(version, *args, **kwargs):
        """Méthode pour créer une tâche."""
        task_factory_map = {
            "v1": TaskV1Factory,
            "v2": TaskV2Factory,
        }

        factory_class = task_factory_map.get(version)
        if factory_class:
            factory = factory_class()
            task = factory.create_task(*args, **kwargs)
            return TaskWithLogging(task)
        raise ValueError(f"Unsupported task version: {version}")
