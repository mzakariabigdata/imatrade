"""Module for the command line interface."""
import os
from dotenv import load_dotenv
import click

from src.imatrade.menu import Menu
from src.imatrade.utils.config import APPLICATION


from src.imatrade.command.add_task_command import (
    AddTaskCommand,
    DisplayStrategyCommand,
    DisplayTasksCommand,
    PerformTasksCommand,
    QuitCommand,
    DisplayAllStrategiesCommand,
    DisplayStrategiesSummaryCommand,
    GetHistoricalDataCommand,
    ProcessMarketDataCommand,
    DisplayAllIndicatorsCommand,
    DisplayIndicatorsSummaryCommand,
    DisplayIndicatorCommand,
    PrepareIndicatorDataCommand,
    LoadDataCommand,
    PrintDataCommand,
    SaveDataCommand,
    PrepareStrategyDataCommand,
    DisplayAllBacktestsCommand,
    DisplayBacktestsSummaryCommand,
    DisplayBacktestCommand,
    RunStrategyCommand,
    RunBacktestCommand,
)

from src.imatrade.data_providers.oanda_data import OandaDataProvider
from src.imatrade.model.report_generator import ReportGenerator


from src.imatrade.controller.task_controller import TaskController
from src.imatrade.strategy.task import TitleSortingStrategy
from src.imatrade.strategy.task import PrioritySortingStrategy

from src.imatrade.observer import TaskCountObserver
from src.imatrade.observer import TaskPriorityObserver
from src.imatrade.observer import TaskDueDateObserver

from src.imatrade.strategy.observer import TaskCountStrategy
from src.imatrade.strategy.observer import TaskPriorityStrategy
from src.imatrade.strategy.observer import TaskDueDateStrategy


from src.imatrade.factory.trading_strategy_factory import TradingStrategyFactory
from src.imatrade.factory.trading_indicators_factory import TradingIndicatorsFactory
from src.imatrade.factory.trading_backtests_factory import TradingBacktestsFactory
from src.imatrade.controller.trading_strategy_controller import (
    TradingStrategyController,
)
from src.imatrade.controller.trading_indicators_controller import (
    TradingIndicatorsController,
)
from src.imatrade.controller.treading_data_controller import TreadingDataController
from src.imatrade.controller.trading_backtest_controller import (
    TradingBacktestController,
)


def display_menu(commands):
    """Display the menu."""
    print("\nOptions :")
    for key, command in commands.items():
        print(f"{key}. {command.description}")


def create_trading_backtest_controller():
    """Create a trading backtest controller."""
    backtests_factory = TradingBacktestsFactory(
        APPLICATION.backtests_config.backtests_composer
    )
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_backtest_controller = TradingBacktestController(
        backtests_factory, treading_data_controller
    )

    return trading_backtest_controller


def create_trading_indicators_controller():
    """Create a trading indicators controller."""
    indicators_factory = TradingIndicatorsFactory(
        APPLICATION.indicators_config.indicators_composer
    )
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_indicators_controller = TradingIndicatorsController(
        indicators_factory, treading_data_controller
    )

    return trading_indicators_controller


def create_trading_strategy_controller():
    """Create a trading strategy controller."""
    strategy_factory = TradingStrategyFactory(
        APPLICATION.strategies_config.strategies_composer
    )
    report_generator = ReportGenerator()
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_strategy_controller = TradingStrategyController(
        strategy_factory, treading_data_controller, report_generator
    )

    return trading_strategy_controller


def create_task_controller():
    """Create a task controller."""
    count_strategy = TaskCountStrategy()
    priority_strategy = TaskPriorityStrategy()
    due_date_strategy = TaskDueDateStrategy()

    count_observer = TaskCountObserver(count_strategy)
    priority_observer = TaskPriorityObserver(priority_strategy)
    due_date_observer = TaskDueDateObserver(due_date_strategy)

    sorting_strategy = TitleSortingStrategy()  # Utiliser la stratégie de tri par titre
    sorting_strategy = (
        PrioritySortingStrategy()
    )  # Utiliser la stratégie de tri par priorité
    task_controller = TaskController(
        sorting_strategy,
        observers=[count_observer, priority_observer, due_date_observer],
    )

    return task_controller


def trade_menu():
    """Trade menu."""
    load_dotenv()

    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))

    #####################
    ###data controller###
    #####################
    # Créer une instance du contrôleur avec la factory
    treading_data_controller = TreadingDataController(oanda_data_provider)

    ################
    #####Tâches#####
    ################

    task_controller = create_task_controller()

    ################
    ###Indicators###
    ################

    trading_indicators_controller = create_trading_indicators_controller()
    # Créer toutes les indicators à partir du fichier indicators.yaml
    indicators = trading_indicators_controller.create_all_indicators()
    print("--- indicators --- ", indicators)

    ################
    ###Strategies###
    ################
    trading_strategy_controller = create_trading_strategy_controller()
    # Créer toutes les stratégies à partir du fichier strategies.yaml
    strategies = trading_strategy_controller.create_all_strategies()
    print("--- strategies --- ", strategies)

    ################
    ####Backtest####
    ################

    # APPLICATION.backtests_config.backtests_composer
    trading_backtest_controller = create_trading_backtest_controller()
    trading_backtest_controller.trading_strategy_controller = (
        trading_strategy_controller
    )
    trading_backtest_controller.create_all_backtests()
    print("--- backtests --- ", trading_backtest_controller.backtests)

    #######################
    ###Données de marché###
    #######################

    ################
    ######Menu######
    ################
    trade_options = {
        "1": "--------- 1. Tasks ---------",
        1_1: AddTaskCommand(task_controller),
        1_2: DisplayTasksCommand(task_controller),
        1_3: PerformTasksCommand(task_controller),
        "2": "--------- 2. Indicators ---------",
        2_1: DisplayIndicatorCommand(trading_indicators_controller),
        2_2: DisplayAllIndicatorsCommand(trading_indicators_controller),
        2_3: DisplayIndicatorsSummaryCommand(trading_indicators_controller),
        2_4: PrepareIndicatorDataCommand(trading_indicators_controller),
        "3": "--------- 3. Strategies ---------",
        3_1: DisplayStrategyCommand(trading_strategy_controller),
        3_2: DisplayAllStrategiesCommand(trading_strategy_controller),
        3_3: DisplayStrategiesSummaryCommand(trading_strategy_controller),
        3_4: PrepareStrategyDataCommand(trading_strategy_controller),
        3_5: RunStrategyCommand(trading_strategy_controller),
        "4": "--------- 4. Backtests ---------",
        4_1: DisplayBacktestCommand(trading_backtest_controller),
        4_2: DisplayAllBacktestsCommand(trading_backtest_controller),
        4_3: DisplayBacktestsSummaryCommand(trading_backtest_controller),
        4_4: RunBacktestCommand(trading_backtest_controller),
        "5": "--------- 5. Market data ---------",
        5_1: GetHistoricalDataCommand(treading_data_controller),
        5_2: ProcessMarketDataCommand(trading_strategy_controller),
        5_3: LoadDataCommand(treading_data_controller),
        5_4: PrintDataCommand(treading_data_controller),
        5_5: SaveDataCommand(treading_data_controller),
        "6": "--------- 6. Quit ---------",
        0: QuitCommand(),
    }

    Menu(trade_options).run()


@click.group()
def config_cmds():
    """Configuration commands."""


@click.group()
def trade_cmds():
    """Trade commands."""


@trade_cmds.command()
def menu():
    """Trade menu."""
    trade_menu()


@trade_cmds.command()
def plan():
    """Trade plan."""
    print("plan")


@trade_cmds.command()
def state():
    """Trade state."""
    print("state")


@config_cmds.command()
def explain():
    """Explain configuration."""
    print("explain")


@config_cmds.command()
def schemas():
    """Configuration schemas."""
    print("schemas")


@config_cmds.command()
def validate():
    """Validate configuration."""
    print("validate")


@click.group()
def cli():
    """Imatrade command line interface."""


@cli.command()
def trade():
    """Trade commands."""
    trade_cmds()


@cli.command()
def config():
    """Configuration commands."""
    config_cmds()


cli.add_command(config_cmds, name="config")
cli.add_command(trade_cmds, name="trade")

if __name__ == "__main__":
    cli()
