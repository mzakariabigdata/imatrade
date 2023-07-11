"""Module for SortingStrategy abstract class."""

from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    """Class for SortingStrategy abstract class."""

    @abstractmethod
    def sort_tasks(self, tasks):
        """Method abstract to sort tasks."""

    def __str__(self):
        return "Tri par défaut"
