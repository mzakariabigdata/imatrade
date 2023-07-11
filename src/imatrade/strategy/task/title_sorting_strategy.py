"""Module for sorting tasks by title."""

from src.imatrade.strategy.task.sorting_strategy import SortingStrategy


class TitleSortingStrategy(SortingStrategy):
    """Class for sorting tasks by title."""

    def sort_tasks(self, tasks):
        return sorted(tasks, key=lambda task: task.title)

    def __str__(self):
        return "Tri par titre"
