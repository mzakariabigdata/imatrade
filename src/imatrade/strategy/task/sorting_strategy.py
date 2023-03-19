from abc import ABC, abstractmethod


class SortingStrategy(ABC):
    @abstractmethod
    def sort_tasks(self, tasks):
        pass
