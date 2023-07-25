"""Module for trading backtest controller."""

from src.imatrade.view.trading_backtest_view import TradingBacktestView


class TradingBacktestController:
    """Class for trading backtest controller."""

    def __init__(self, backtest_factory, data_controller):
        self.backtest_factory = backtest_factory  # Factory des backtests
        self.data_controller = data_controller  # Contrôleur des données
        self.backtests = {}  # Dictionnaire des backtests

    # def backtest(self, strategy_name):
    #     """Method to backtest a strategy."""
    #     self.trading_strategy_controller.backtest(strategy_name)

    def run_backtest(self, backtest_name):
        """Method to run a backtest."""
        self.backtests.get(backtest_name).run()

    def load_backtests_builder(self):
        """Method to load backtests builder."""
        self.backtest_factory.load_builder()  # Charger les constructeurs de backtests

    def create_all_backtests(self):
        """Method to create all backtests."""
        self.load_backtests_builder()
        for (
            backtest_name
        ) in (
            self.backtest_factory.get_registered_backtest_names()
        ):  # Créer tous les backtests
            backtest = self.backtest_factory.create_backtest(
                backtest_name
            )  # Créer un backtest
            self.add_backtest(
                backtest_name, backtest
            )  # Ajouter le backtest au dictionnaire
        return self.backtests  # Retourner les backtests

    def create_backtest(self, backtest_type):
        """Method to create a backtest."""
        backtest_name, backtest = self.backtest_factory.create_backtest(backtest_type)
        self.add_backtest(backtest_name, backtest)
        return backtest

    def add_backtest(self, backtest_name, backtest):
        """Method to add a backtest to the dictionary."""
        self.backtests[backtest_name] = backtest

    def remove_backtest(self, backtest_name):
        """Method to remove a backtest."""
        if backtest_name in self.backtests:
            del self.backtests[backtest_name]

    def display_all_backtests(self):
        """Method to display all backtests."""
        TradingBacktestView.display_all_backtests(self.backtests)

    def display_backtests_summary(self):
        """Method to display backtests summary."""
        TradingBacktestView.display_backtests_summary(self.backtests)

    def display_backtest(self, backtest_name):
        """Method to display a backtest."""
        TradingBacktestView.display_backtest(self.backtests.get(backtest_name) or None)
