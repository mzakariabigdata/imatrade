from .task_command import TaskCommand


class AddTaskCommand(TaskCommand):
    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        return "Ajouter une tâche"

    def execute(self):
        self.task_controller.add_task()


class DisplayTasksCommand(TaskCommand):
    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        return "Afficher les tâches"

    def execute(self):
        self.task_controller.display_tasks()


class DisplayStrategySummary(TaskCommand):
    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        return "Récapitulatif des stratégies de trading"

    def execute(self):
        self.task_controller.display_strategy_summary()


class PerformTasksCommand(TaskCommand):
    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        return "Perform les tâches"

    def execute(self):
        self.task_controller.perform_tasks()


class GetHistoricalDataCommand(TaskCommand):
    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        return "Get historical data"

    def execute(self):
        self.task_controller.get_historical_data()


class DisplayStrategyCommand(TaskCommand):
    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        return "Afficher la stratégie"

    def execute(self):
        strategy_name = input("Entrez Strategy name : ")
        self.trading_strategy_controller.display_strategy(strategy_name)


class DisplayAllStrategiesCommand(TaskCommand):
    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        return "Afficher toutes les stratégies"

    def execute(self):
        self.trading_strategy_controller.display_all_strategies()


class ProcessMarketDataCommand(TaskCommand):
    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        return "Market Data Processor"

    def execute(self):
        self.trading_strategy_controller.process_market_data()


class QuitCommand(TaskCommand):
    description = "Quitter"

    def execute(self):
        print("Au revoir !")
        exit(0)
