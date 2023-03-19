from imatrade.command.task_command import TaskCommand


class AddTaskCommand(TaskCommand):
    def __init__(self, task_controller, task):
        self.task_controller = task_controller
        self.task = task

    def execute(self):
        self.task_controller.add_task(self.task)

    def undo(self):
        self.task_controller.remove_task(self.task)
