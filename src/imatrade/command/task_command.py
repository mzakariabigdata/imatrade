from abc import ABC, abstractmethod


class TaskCommand(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError