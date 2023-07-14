"""Contains the TradingBacktest class."""

from imobject import ObjDict

# add runners to the backtest


# class ITradingBacktest(ABC):
#     """Abstract class for trading backtests."""

#     @abstractmethod
#     def run(self):
#         """Abstract method to run a trading backtest."""
#         pass


class TradingBacktest:
    """Class for trading backtests."""

    def __init__(self, **kwargs):
        self._kwargs = ObjDict(kwargs)
        self.name = self._kwargs.name
        self.display_name = self._kwargs.display_name
        self.description = self._kwargs.description
        self.strategies = self._kwargs.strategies

    def run(self):
        """Method to run a trading backtest."""
        print(f"Running backtest: {self.name}")
        print(f"Display name: {self.display_name}")
        print(f"Description: {self.description}")
        print(f"Strategies: {self.strategies}")
        print()
        for strategy in self.strategies:
            strategy.run()

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"
