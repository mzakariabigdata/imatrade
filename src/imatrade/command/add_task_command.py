"""Module for the command pattern used to execute tasks.
"""
import sys
from .task_command import TaskCommand


class AddTaskCommand(TaskCommand):
    """Class for adding a task."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Ajouter une tâche"

    def execute(self):
        """Execute the command."""
        self.task_controller.add_task()


class DisplayTasksCommand(TaskCommand):
    """Class for displaying tasks."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Afficher les tâches"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_tasks()


class DisplayStrategySummary(TaskCommand):
    """Class for displaying strategy summary."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Récapitulatif des stratégies de trading"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_strategy_summary()


class PerformTasksCommand(TaskCommand):
    """Class for performing tasks."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Perform les tâches"

    def execute(self):
        """Execute the command."""
        self.task_controller.perform_tasks()


class GetHistoricalDataCommand(TaskCommand):
    """Class for getting historical data."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Get historical data"

    def execute(self):
        """Execute the command."""
        self.task_controller.get_historical_data()


class DisplayStrategyCommand(TaskCommand):
    """Class for displaying a strategy."""

    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Afficher la stratégie"

    def execute(self):
        """Execute the command."""
        strategy_name = input("Entrez Strategy name : ")
        self.trading_strategy_controller.display_strategy(strategy_name)


class DisplayAllStrategiesCommand(TaskCommand):
    """Class for displaying all strategies."""

    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Afficher toutes les stratégies"

    def execute(self):
        """Execute the command."""
        self.trading_strategy_controller.display_all_strategies()


class ProcessMarketDataCommand(TaskCommand):
    """Class for processing market data."""

    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Market Data Processor"

    def execute(self):
        """Execute the command."""
        self.trading_strategy_controller.process_market_data()


class QuitCommand(TaskCommand):
    """Class for quitting the program."""

    @property
    def description(self):
        """Return the description of the command."""
        return "Quitter"

    def execute(self):
        """Execute the command."""
        print("Au revoir !")
        sys.exit(0)
