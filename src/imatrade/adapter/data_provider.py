"""Module for DataProvider abstract class."""
from abc import ABC, abstractmethod


class DataProvider(ABC):
    """Class for DataProvider abstract class."""

    @abstractmethod
    def get_historical_data(self, instrument, start, end, granularity):
        """Method abstract to get historical data."""

    @abstractmethod
    def get_current_price(self, instrument):
        """Method abstract to get current price."""
