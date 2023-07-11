"""Module pour la vue des tâches"""


class TaskView:
    """Vue pour les tâches"""

    @staticmethod
    def display_tasks(tasks):
        """Affiche les tâches"""
        print("Liste des tâches :")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")

    @staticmethod
    def perform_tasks(tasks):
        """Effectue les tâches"""
        print("Perform des tâches :")
        for i, task in enumerate(tasks, start=1):
            print("-" * 10)
            print(f"{i}. Perform task: {task.title}")
            task.perform_task()
            print("-" * 10)

    @staticmethod
    def get_task_title():
        """Demande le titre de la tâche"""
        return input("Entrez le titre de la tâche : ")

    @staticmethod
    def get_task_description():
        """Demande la description de la tâche"""
        return input("Entrez la description de la tâche : ")

    @staticmethod
    def get_task_priority():
        """Demande la priorité de la tâche"""
        return int(input("Entrez la priorité de la tâche (1-5) : "))
