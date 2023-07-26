"""Module for DataProvider abstract class."""
from abc import ABC, abstractmethod


class DataProvider(ABC):  # pylint: disable=too-few-public-methods
    """Class for DataProvider abstract class."""

    @abstractmethod
    def get_history(self, instrument, start, end, granularity):
        """Method abstract to get historical data."""
