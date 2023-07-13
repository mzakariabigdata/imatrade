"""Module for the command line interface."""
import os
import pandas as pd
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
    DisplayStrategiesSummary,
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
)

from src.imatrade.data_providers.oanda_data import OandaDataProvider

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
from src.imatrade.controller.trading_strategy_controller import (
    TradingStrategyController,
)
from src.imatrade.controller.trading_indicators_controller import (
    TradingIndicatorsController,
)
from src.imatrade.controller.treading_data_controller import TreadingDataController


def display_menu(commands):
    """Display the menu."""
    print("\nOptions :")
    for key, command in commands.items():
        print(f"{key}. {command.description}")


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

    ################
    ###Indicators###
    ################
    # Créer une instance de la factory TradingStrategyFactory avec les stratégies disponibles
    indicators_factory = TradingIndicatorsFactory(
        APPLICATION.indicators_config.indicators_composer
    )
    # Créer une instance du contrôleur avec la factory
    trading_indicators_controller = TradingIndicatorsController(
        indicators_factory, treading_data_controller
    )
    # load all indicators builders
    # trading_indicators_controller.load_indicators_builder()
    # Créer toutes les indicators à partir du fichier indicators.yaml
    indicators = trading_indicators_controller.create_all_indicators()
    print("--- indicators --- ", indicators)

    ################
    ###Strategies###
    ################
    # Créer une instance de la factory TradingStrategyFactory avec les stratégies disponibles
    strategy_factory = TradingStrategyFactory(
        APPLICATION.strategies_config.strategies_composer
    )
    # Créer une instance du contrôleur avec la factory
    trading_strategy_controller = TradingStrategyController(
        strategy_factory, treading_data_controller
    )
    # # load all strategies builders
    # trading_strategy_controller.load_strategies_builder()
    # Créer toutes les stratégies à partir du fichier strategies.yaml
    strategies = trading_strategy_controller.create_all_strategies()
    print("--- strategies --- ", strategies)

    #######################
    ###Données de marché###
    #######################

    # Exemple de données de marché
    market_data = [
        {
            "date": "2021-01-01",
            "open": 1.2345,
            "close": 1.2360,
            "high": 1.2360,
            "low": 1.2380,
        },
        {
            "date": "2021-01-02",
            "open": 1.2350,
            "close": 1.2380,
            "high": 1.2380,
            "low": 1.2380,
        },
        {
            "date": "2022-01-01",
            "open": 1.2380,
            "close": 1.2350,
            "high": 1.2390,
            "low": 1.2310,
        },
        {
            "date": "2022-01-02",
            "open": 1.2340,
            "close": 1.2320,
            "high": 1.2380,
            "low": 1.2300,
        },
        {
            "date": "2022-01-03",
            "open": 1.2320,
            "close": 1.2340,
            "high": 1.2350,
            "low": 1.2300,
        },
        {
            "date": "2022-01-04",
            "open": 1.2330,
            "close": 1.2325,
            "high": 1.2370,
            "low": 1.2310,
        },
        {
            "date": "2022-01-05",
            "open": 1.2325,
            "close": 1.2310,
            "high": 1.2340,
            "low": 1.2290,
        },
        {
            "date": "2022-01-06",
            "open": 1.2310,
            "close": 1.2325,
            "high": 1.2335,
            "low": 1.2280,
        },
        {
            "date": "2022-01-07",
            "open": 1.2325,
            "close": 1.2315,
            "high": 1.2330,
            "low": 1.2295,
        },
        {
            "date": "2022-01-08",
            "open": 1.2315,
            "close": 1.2335,
            "high": 1.2345,
            "low": 1.2310,
        },
        {
            "date": "2022-01-09",
            "open": 1.2335,
            "close": 1.2350,
            "high": 1.2370,
            "low": 1.2325,
        },
        {
            "date": "2022-01-10",
            "open": 1.2350,
            "close": 1.2330,
            "high": 1.2375,
            "low": 1.2325,
        },
        {
            "date": "2022-01-11",
            "open": 1.2330,
            "close": 1.2345,
            "high": 1.2365,
            "low": 1.2315,
        },
        {
            "date": "2022-01-12",
            "open": 1.2345,
            "close": 1.2360,
            "high": 1.2365,
            "low": 1.2325,
        },
        {
            "date": "2022-01-13",
            "open": 1.2360,
            "close": 1.2370,
            "high": 1.2385,
            "low": 1.2335,
        },
    ]
    # Convertir la liste de dictionnaires en DataFrame pandas
    market_data = pd.DataFrame(market_data)
    # Convertir la colonne "date" en objet datetime
    market_data["date"] = pd.to_datetime(market_data["date"])
    # Définir la colonne "date" comme index
    market_data.set_index("date", inplace=True)
    # Exécuter les stratégies et afficher les signaux de trading
    # for strategy_name, _ in strategies.items():
    #     trading_strategy_controller.execute_strategy(strategy_name, market_data)

    ################
    ######Menu######
    ################
    commands = {
        "1": "---------1. Tasks---------",
        1_1: AddTaskCommand(task_controller),
        1_2: DisplayTasksCommand(task_controller),
        1_3: PerformTasksCommand(task_controller),
        "2": "---------2. Indicators---------",
        2_1: DisplayIndicatorCommand(trading_indicators_controller),
        2_2: DisplayAllIndicatorsCommand(trading_indicators_controller),
        2_3: DisplayIndicatorsSummaryCommand(trading_indicators_controller),
        2_4: PrepareIndicatorDataCommand(trading_indicators_controller),
        "3": "---------3. Strategies---------",
        3_1: DisplayStrategyCommand(trading_strategy_controller),
        3_2: DisplayAllStrategiesCommand(trading_strategy_controller),
        3_3: DisplayStrategiesSummary(trading_strategy_controller),
        3_4: PrepareStrategyDataCommand(trading_strategy_controller),
        "4": "---------4. Market data---------",
        4_1: GetHistoricalDataCommand(treading_data_controller),
        4_2: ProcessMarketDataCommand(trading_strategy_controller),
        4_3: LoadDataCommand(treading_data_controller),
        4_4: PrintDataCommand(treading_data_controller),
        4_5: SaveDataCommand(treading_data_controller),
        "5": "---------5. Quit---------",
        0: QuitCommand(),
    }

    trade_options = Menu(commands)
    trade_options.run()


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
