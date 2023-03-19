class TaskView:
    @staticmethod
    def display_tasks(tasks):
        print("Liste des tâches :")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

    @staticmethod
    def perform_tasks(tasks):
        print("Perform des tâches :")
        for i, task in enumerate(tasks, start=1):
            print("-" * 10)
            print(f"{i}. Perform task: {task.title}")
            task.perform_task()
            print("-" * 10)

    @staticmethod
    def get_task_title():
        return input("Entrez le titre de la tâche : ")

    @staticmethod
    def get_task_description():
        return input("Entrez la description de la tâche : ")

    @staticmethod
    def get_task_priority():
        return int(input("Entrez la priorité de la tâche (1-5) : "))
