import pandas as pd
import os
from dotenv import load_dotenv

from imatrade.menu import Menu

from imatrade.utils.config import APPLICATION

from imatrade.command.add_task_command import (
    AddTaskCommand,
    DisplayStrategyCommand,
    DisplayTasksCommand,
    PerformTasksCommand,
    QuitCommand,
    DisplayAllStrategiesCommand,
    DisplayStrategySummary,
    GetHistoricalDataCommand
)

from imatrade.data_providers.oanda_data import OandaDataProvider

from imatrade.controller.task_controller import TaskController
from imatrade.strategy.task import TitleSortingStrategy
from imatrade.strategy.task import PrioritySortingStrategy

from imatrade.observer import TaskCountObserver
from imatrade.observer import TaskPriorityObserver
from imatrade.observer import TaskDueDateObserver

from imatrade.strategy.observer import TaskCountStrategy
from imatrade.strategy.observer import TaskPriorityStrategy
from imatrade.strategy.observer import TaskDueDateStrategy


from imatrade.model.trading_strategy_builder import (
    MACrossoverStrategyBuilder,
    RSIStrategyBuilder,
    BollingerBandsStrategyBuilder,
    StochasticOscillatorStrategyBuilder,
    ATRStrategyBuilder,
    MACDStrategyBuilder,
    IchimokuCloudStrategyBuilder,
    MAEnvelopeStrategyBuilder,
    RSIDivergenceStrategyBuilder,
    BreakoutStrategyBuilder
)
from imatrade.factory.trading_strategy_factory import TradingStrategyFactory
from imatrade.controller.trading_strategy_controller import TradingStrategyController


def display_menu(commands):
    print("\nOptions :")
    for key, command in commands.items():
        print(f"{key}. {command.description}")


def main():
    load_dotenv()

    oanda_data_provider = OandaDataProvider(api_key=os.getenv('OANDA_API_KEY'))

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

    # Créer une instance de la factory TradingStrategyFactory avec les stratégies disponibles
    strategy_factory = TradingStrategyFactory()
    # Créer une instance du contrôleur avec la factory
    trading_strategy_controller = TradingStrategyController(strategy_factory, oanda_data_provider)
    # load all strategies builders
    trading_strategy_controller.load_strategies_builders()
    # Créer toutes les stratégies à partir du fichier strategies.yaml
    strategies = trading_strategy_controller.create_all_strategies()
    print("--- strategies --- ", strategies)

    # Créer une stratégie de trading en utilisant la factory
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
        "low": 1.2310
    },
    {
        "date": "2022-01-02",
        "open": 1.2340,
        "close": 1.2320,
        "high": 1.2380,
        "low": 1.2300
    },
    {
        "date": "2022-01-03",
        "open": 1.2320,
        "close": 1.2340,
        "high": 1.2350,
        "low": 1.2300
    },
    {
        "date": "2022-01-04",
        "open": 1.2330,
        "close": 1.2325,
        "high": 1.2370,
        "low": 1.2310
    },
    {
        "date": "2022-01-05",
        "open": 1.2325,
        "close": 1.2310,
        "high": 1.2340,
        "low": 1.2290
    },
    {
        "date": "2022-01-06",
        "open": 1.2310,
        "close": 1.2325,
        "high": 1.2335,
        "low": 1.2280
    },
    {
        "date": "2022-01-07",
        "open": 1.2325,
        "close": 1.2315,
        "high": 1.2330,
        "low": 1.2295
    },
    {
        "date": "2022-01-08",
        "open": 1.2315,
        "close": 1.2335,
        "high": 1.2345,
        "low": 1.2310
    },
    {
        "date": "2022-01-09",
        "open": 1.2335,
        "close": 1.2350,
        "high": 1.2370,
        "low": 1.2325
    },
    {
        "date": "2022-01-10",
        "open": 1.2350,
        "close": 1.2330,
        "high": 1.2375,
        "low": 1.2325
    },
    {
        "date": "2022-01-11",
        "open": 1.2330,
        "close": 1.2345,
        "high": 1.2365,
        "low": 1.2315
    },
    {
        "date": "2022-01-12",
        "open": 1.2345,
        "close": 1.2360,
        "high": 1.2365,
        "low": 1.2325
    },
    {
        "date": "2022-01-13",
        "open": 1.2360,
        "close": 1.2370,
        "high": 1.2385,
        "low": 1.2335
    },
    ]
    # Convertir la liste de dictionnaires en DataFrame pandas
    market_data = pd.DataFrame(market_data)
    # Convertir la colonne "date" en objet datetime
    market_data["date"] = pd.to_datetime(market_data["date"])
    # Définir la colonne "date" comme index
    market_data.set_index("date", inplace=True)
    # Exécuter les stratégies et afficher les signaux de trading
    for strategy_name, strategy in strategies.items():
        trading_strategy_controller.execute_strategy(strategy_name, market_data)

    commands = {
        1: AddTaskCommand(task_controller),
        2: DisplayTasksCommand(task_controller),
        3: PerformTasksCommand(task_controller),
        4: DisplayStrategyCommand(trading_strategy_controller),
        5: DisplayAllStrategiesCommand(trading_strategy_controller),
        6: DisplayStrategySummary(trading_strategy_controller),
        7: GetHistoricalDataCommand(trading_strategy_controller),
        0: QuitCommand(),
    }

    menu = Menu(commands)
    menu.run()


if __name__ == "__main__":
    main()
