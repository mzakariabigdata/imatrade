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


class DisplayStrategiesSummary(TaskCommand):
    """Class for displaying strategy summary."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display strategies summary"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_strategies_summary()


class DisplayIndicatorsSummaryCommand(TaskCommand):
    """Class for displaying indicators summary."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display indicators summary"

    def execute(self):
        """Execute the command."""
        self.task_controller.display_indicators_summary()


class PrepareIndicatorCommand(TaskCommand):
    """Class for performing indicators."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Prepare indicator"

    def execute(self):
        """Execute the command."""
        indicator_name = input("Name of the indicator: ")
        if not indicator_name:
            indicator_name = "BollingerBands"
        self.task_controller.prepare_indicator(indicator_name)


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


class LoadDataCommand(TaskCommand):
    """Class for loading data."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Load data"

    def execute(self):
        """Execute the command."""
        num_file = input("Number of file: ")
        if not num_file:
            num_file = 1
        self.task_controller.load_data(num_file)


class PrintDataCommand(TaskCommand):
    """Class for printing data."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Print data"

    def execute(self):
        """Execute the command."""
        self.task_controller.print_data()


class SaveDataCommand(TaskCommand):
    """Class for saving data."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Save data"

    def execute(self):
        """Execute the command."""
        self.task_controller.save_data()


class DisplayIndicatorCommand(TaskCommand):
    """Class for displaying an indicator."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display an indicator"

    def execute(self):
        """Execute the command."""
        indicator_name = input("Name of the indicator: ")
        self.task_controller.display_indicator(indicator_name)


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
