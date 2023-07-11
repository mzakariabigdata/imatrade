"""Module for processing market data."""

import pandas as pd
from src.imatrade.model.tick import Tick


class TickHandler:  # pylint: disable=too-few-public-methods
    """Class for handling ticks."""

    def __init__(self, strategies):
        self.strategies = strategies

    def on_tick(self, timestamp, price, volume):
        """Method for handling tick."""
        tick = Tick(timestamp, price, volume)

        for strategy in self.strategies:
            strategy.handle_tick(tick)


class MarketDataProcessor:  # pylint: disable=too-few-public-methods
    """Class for processing market data."""

    def __init__(self, data_frame: pd.DataFrame, strategies):
        self.data_frame = data_frame
        self.tick_handler = TickHandler(strategies)

    def process_data(self):
        """Method for processing data."""
        for _, row in self.data_frame.iterrows():
            timestamp = row["timestamp"]
            price = row["price"]
            volume = row["volume"]
            self.tick_handler.on_tick(timestamp, price, volume)
