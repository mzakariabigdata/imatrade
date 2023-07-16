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


class DisplayBacktestsSummaryCommand(TaskCommand):
    """Class for displaying backtests."""

    def __init__(self, backtest_controller):
        self.backtest_controller = backtest_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display backtests summary"

    def execute(self):
        """Execute the command."""
        self.backtest_controller.display_backtests_summary()


class DisplayBacktestCommand(TaskCommand):
    """Class for displaying a backtest."""

    def __init__(self, backtest_controller):
        self.backtest_controller = backtest_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display a backtest"

    def execute(self):
        """Execute the command."""
        backtest_name = input("Name of the backtest: ")
        if not backtest_name:
            backtest_name = "dolar_euro_macd"
        self.backtest_controller.display_backtest(backtest_name)


class DisplayStrategiesSummaryCommand(TaskCommand):
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


class PrepareStrategyDataCommand(TaskCommand):
    """Class for preparing a strategy."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Prepare strategy data"

    def execute(self):
        """Execute the command."""
        strategy_name = input("Name of the strategy: ")
        if not strategy_name:
            strategy_name = "BollingerBands"
        self.task_controller.prepare_strategy_data(strategy_name)


class PrepareIndicatorDataCommand(TaskCommand):
    """Class for preparing data for an indicator."""

    def __init__(self, task_controller):
        self.task_controller = task_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Prepare indicator data"

    def execute(self):
        """Execute the command."""
        indicator_name = input("Name of the indicator: ")
        if not indicator_name:
            indicator_name = "BollingerBands"
        self.task_controller.prepare_indicator_data(indicator_name)


class DisplayAllBacktestsCommand(TaskCommand):
    """Class for displaying all backtests."""

    def __init__(self, backtest_controller):
        self.backtest_controller = backtest_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Display all backtests"

    def execute(self):
        """Execute the command."""
        self.backtest_controller.display_all_backtests()


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
        if not strategy_name:
            strategy_name = "BollingerBands"
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


class RunStrategyCommand(TaskCommand):
    """Class for running a strategy."""

    def __init__(self, trading_strategy_controller):
        self.trading_strategy_controller = trading_strategy_controller

    @property
    def description(self):
        """Return the description of the command."""
        return "Run a strategy"

    def execute(self):
        """Execute the command."""
        strategy_name = input("Name of the strategy: ")
        if not strategy_name:
            strategy_name = "MACD"
        self.trading_strategy_controller.run_strategy(strategy_name)


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
        strategy_name = input("Name of the strategy: ")
        if not strategy_name:
            strategy_name = "RSIStrategy"
        self.trading_strategy_controller.process_market_data(strategy_name)


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
