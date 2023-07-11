"""Module for priority sorting strategy."""

from src.imatrade.strategy.task.sorting_strategy import SortingStrategy


class PrioritySortingStrategy(
    SortingStrategy
):  # pylint: disable=too-few-public-methods
    """Class for priority sorting strategy."""

    def sort_tasks(self, tasks):
        return sorted(tasks, key=lambda task: task.priority_level)
