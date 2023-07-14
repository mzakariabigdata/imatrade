"""Module for trading backtests factory."""


import importlib


class TradingBacktestsFactory:
    """Class for trading backtests factory."""

    def __init__(self, backtests_composer):
        self.backtests_composer = backtests_composer
        self._builder = None
        self.backtests = []

    def load_builder(self):
        """Method to load backtests builder."""
        module = importlib.import_module("src.imatrade.model.trading_backtest_builder")
        builder_class = getattr(module, "TradingBacktestBuilder")

        builder_instance = builder_class()
        self._builder = builder_instance

        self.load_backtests()

    def load_backtests(self):
        """Method to load backtests."""
        for backtest in self.backtests_composer.backtests:
            self.backtests.append(backtest["name"])

    def get_registered_backtest_names(self):
        """Method to get registered backtest names."""
        return self.backtests

    def create_backtest(self, backtest_name: str):
        """Method to create a backtest.

        Args:
            backtest_name (str):  Name of the backtest.

        Raises:
            ValueError:  If the name of the backtest is not valid.

        Returns:
            _type_:  Backtest.
        """
        if not self._builder:
            raise ValueError("Builder not loaded")
        if backtest_name not in self.backtests:
            raise ValueError(f"Invalid backtest name: {backtest_name}")
        backtest_config = self.backtests_composer.backtests.where(name=backtest_name)
        return self._builder.build(backtest_config)[0]

    # def create_all_backtests(self):
    #     """Method to create all backtests."""
    #     self.load_builder()
    #     for backtest_name in self.backtests_composer.backtests:
    #         backtest = self.create_backtest(backtest_name)
    #         self.add_backtest(backtest_name, backtest)
    #     return self.backtests

    # def add_backtest(self, backtest_name, backtest):
    #     """Method to add a backtest to the dictionary."""
    #     self.backtests[backtest_name] = backtest

    # def create_backtest(self, backtest_type):
    #     """Method to create a backtest."""
    #     backtest_name, backtest = self.backtests[backtest_type]()
    #     return backtest
