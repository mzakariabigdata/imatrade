import pandas as pd

from imatrade.utils.config import strategies_config

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
    controller = TradingStrategyController(strategy_factory)
    # Créer une stratégie de trading en utilisant la factory
    ma_crossover_config = strategies_config.get("MA_Crossover")
    ma_crossover_strategy = controller.create_strategy(
        "MA_Crossover",
        short_window=ma_crossover_config["short_window"],
        long_window=ma_crossover_config["long_window"],
    )
    rsi_config = strategies_config.get("RSI")
    rsi_strategy = controller.create_strategy(
        "RSI",
        rsi_period=rsi_config["rsi_period"],
        oversold=rsi_config["oversold"],
        overbought=rsi_config["overbought"],
    )
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
    controller.execute_strategy(ma_crossover_strategy, market_data)
    controller.execute_strategy(rsi_strategy, market_data)

    while True:
        print("\nOptions :")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Perform les tâches")
        print("4. Quitter")

        choice = int(input("Choisissez une option : "))

        if choice == 1:
            task_controller.add_task()
        elif choice == 2:
            task_controller.display_tasks()
        elif choice == 3:
            task_controller.perform_tasks()
        elif choice == 4:
            break
        else:
            print("Option invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
