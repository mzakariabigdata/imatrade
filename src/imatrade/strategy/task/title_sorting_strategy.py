from imatrade.strategy.task.sorting_strategy import SortingStrategy


class TitleSortingStrategy(SortingStrategy):
    def sort_tasks(self, tasks):
        return sorted(tasks, key=lambda task: task.title)
