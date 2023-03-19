from imatrade.controller.task_controller import TaskController
from imatrade.strategy.task import TitleSortingStrategy
from imatrade.strategy.task import PrioritySortingStrategy

from imatrade.observer import TaskCountObserver
from imatrade.observer import TaskPriorityObserver
from imatrade.observer import TaskDueDateObserver

from imatrade.strategy.observer import TaskCountStrategy
from imatrade.strategy.observer import TaskPriorityStrategy
from imatrade.strategy.observer import TaskDueDateStrategy


def main():
    count_strategy = TaskCountStrategy()
    priority_strategy = TaskPriorityStrategy()
    due_date_strategy = TaskDueDateStrategy()

    count_observer = TaskCountObserver(count_strategy)
    priority_observer = TaskPriorityObserver(priority_strategy)
    due_date_observer = TaskDueDateObserver(due_date_strategy)

    sorting_strategy = (
        PrioritySortingStrategy()
    )  # Utiliser la stratégie de tri par priorité
    task_controller = TaskController(
        sorting_strategy,
        observers=[count_observer, priority_observer, due_date_observer],
    )

    while True:
        print("\nOptions :")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Perform les tâches")
        print("4. Quitter")

        choice = int(input("Choisissez une option : "))

        if choice == 1:
            task_controller.add_task()
        elif choice == 2:
            task_controller.display_tasks()
        elif choice == 3:
            task_controller.perform_tasks()
        elif choice == 4:
            break
        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
