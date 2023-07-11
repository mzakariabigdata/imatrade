"""Module for TaskCommand abstract class."""
from abc import ABC, abstractmethod


class TaskCommand(ABC):  # pylint: disable=too-few-public-methods
    """Class for TaskCommand abstract class."""

    @abstractmethod
    def execute(self):
        """Method to execute the command."""
        raise NotImplementedError
