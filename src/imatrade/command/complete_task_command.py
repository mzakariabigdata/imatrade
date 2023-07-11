"""Module for the CompleteTaskCommand class."""
from src.imatrade.command.task_command import TaskCommand


class CompleteTaskCommand(TaskCommand):
    """Class for CompleteTaskCommand."""

    def __init__(self, task):
        self.task = task

    def execute(self):
        """Method to execute the command."""
        self.task.complete()

    def undo(self):
        """Method to undo the command."""
        self.task.uncomplete()
