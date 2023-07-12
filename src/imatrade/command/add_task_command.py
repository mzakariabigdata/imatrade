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
        return "Add a task"
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
        return "Display tasks"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_tasks()


class DisplayIndicatorsCommand(TaskCommand):
    """Class for displaying indicators."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display indicators"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_indicators()

class DisplayStrategySummary(TaskCommand):
    """Class for displaying strategy summary."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display strategy summary"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_strategy_summary()

class DisplayAllIndicatorsCommand(TaskCommand):
    """Class for displaying all indicators."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display all indicators"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_all_indicators()

class PerformTasksCommand(TaskCommand):
    """Class for performing tasks."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Perform tasks"

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
        return "Display a strategy"

    def execute(self):
        """Execute the command."""
        strategy_name = input("Name of the strategy: ")
        self.trading_strategy_controller.display_strategy(strategy_name)


class DisplayAllStrategiesCommand(TaskCommand):
    """Class for displaying all strategies."""

    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display all strategies"

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
        print("Quitting...")
        sys.exit(0)
