from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def get_historical_data(self, instrument, start, end, granularity):
        pass