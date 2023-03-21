try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.shortcuts import button_dialog
except ImportError:
    print("Veuillez installer prompt_toolkit pour utiliser cette interface : pip install prompt_toolkit")
    exit(1)
    
import pandas as pd

from imatrade.menu import Menu

from imatrade.utils.config import strategies_config

from imatrade.command.add_task_command import AddTaskCommand, DisplayStrategyCommand, DisplayTasksCommand, PerformTasksCommand, QuitCommand, DisplayAllStrategiesCommand

from imatrade.controller.task_controller import TaskController
from imatrade.strategy.task import TitleSortingStrategy
from imatrade.strategy.task import PrioritySortingStrategy

from imatrade.observer import TaskCountObserver
from imatrade.observer import TaskPriorityObserver
from imatrade.observer import TaskDueDateObserver

from imatrade.strategy.observer import TaskCountStrategy
from imatrade.strategy.observer import TaskPriorityStrategy
from imatrade.strategy.observer import TaskDueDateStrategy


from imatrade.model.trading_strategy_builder import MACrossoverStrategyBuilder, RSIStrategyBuilder
from imatrade.factory.trading_strategy_factory import TradingStrategyFactory
from imatrade.controller.trading_strategy_controller import TradingStrategyController


def display_menu(commands):
    print("\nOptions :")
    for key, command in commands.items():
        print(f"{key}. {command.description}")

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

    # Créer une instance de la factory TradingStrategyFactory avec les stratégies disponibles
    strategy_factory = TradingStrategyFactory()
    strategy_factory.register_builder("MA_Crossover", MACrossoverStrategyBuilder())
    strategy_factory.register_builder("RSI", RSIStrategyBuilder())
    # Créer une instance du contrôleur avec la factory
    trading_strategy_controller = TradingStrategyController(strategy_factory)
    # Créer toutes les stratégies à partir du fichier strategies.yaml
    strategies = trading_strategy_controller.create_all_strategies()
    print(strategies)
    # Créer une stratégie de trading en utilisant la factory
    # Exemple de données de marché
    market_data = [
        {"date": "2021-01-01", "open": 1.2345, "close": 1.2360},
        {"date": "2021-01-02", "open": 1.2350, "close": 1.2380},
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
        6: QuitCommand(),
    }
    
    menu = Menu(commands)
    menu.run()


if __name__ == "__main__":
    main()
