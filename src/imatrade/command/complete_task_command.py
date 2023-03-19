from imatrade.command.task_command import TaskCommand


class CompleteTaskCommand(TaskCommand):
    def __init__(self, task):
        self.task = task

    def execute(self):
        self.task.complete()

    def undo(self):
        self.task.uncomplete()
