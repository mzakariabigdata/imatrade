from imatrade.model import Task, TaskV1, TaskV2
from imatrade.model import TaskBuilder
from imatrade.decorator.task_decorator import TaskWithLogging
from abc import ABC


class TaskFactory:
    """
    Factory pour créer des instances de tâches.
    """

    @staticmethod
    def create_task(title, priority):
        return TaskBuilder().set_title(title).set_priority(priority).build()


class TaskV1Factory(TaskFactory):
    """
    Factory pour créer des instances de tâches de version 1.
    """

    def create_task(self, title, description, priority_level):
        return TaskV1(title, description, priority_level)


class TaskV2Factory(TaskFactory):
    """
    Factory pour créer des instances de tâches de version 2.
    """

    def create_task(self, title, description, due_date):
        return TaskV2(title, description, due_date)


class ExtendedTaskFactory:
    """
    Factory étendue pour créer des instances de tâches en fonction de la version.
    """

    @staticmethod
    def create_task(version, *args, **kwargs):
        task_factory_map = {
            "v1": TaskV1Factory,
            "v2": TaskV2Factory,
        }

        factory_class = task_factory_map.get(version)
        if factory_class:
            factory = factory_class()
            task = factory.create_task(*args, **kwargs)
            return TaskWithLogging(task)
        else:
            raise ValueError(f"Unsupported task version: {version}")
