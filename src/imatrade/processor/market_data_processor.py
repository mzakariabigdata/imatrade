"""Module for processing market data."""

import pandas as pd
from src.imatrade.model.tick import Tick
from collections import deque


class TickHandler:  # pylint: disable=too-few-public-methods
    """Class for handling ticks."""

    def __init__(self, strategies):
        self.strategies = strategies

    def on_tick(
        self, timestamp, open_price, high_price, low_price, close_price, volume
    ):
        """Method for handling tick."""
        tick = Tick(timestamp, open_price, high_price, low_price, close_price, volume)

        for strategy in self.strategies:
            strategy.handle_tick(tick)

    def on_bar(self, timestamp, open_price, high_price, low_price, close_price, volume):
        """Method for handling bar."""
        bar = pd.Series(
            index=["open", "high", "low", "close", "volume"],
            data=[open_price, high_price, low_price, close_price, volume],
        )

        for strategy in self.strategies:
            strategy.handle_bar(bar)


class MarketDataProcessor:  # pylint: disable=too-few-public-methods
    """Class for processing market data."""

    def __init__(self, data_frame: pd.DataFrame, strategy=None):
        self.data_frame = data_frame
        self.tick_handler = TickHandler(strategy)
        self.window_size = 20
        self.window_data = deque(maxlen=self.window_size)

    def set_data_frame(self, data_frame):
        """Method for setting data frame."""
        self.data_frame = data_frame

    def simulate_real_time_data(self, df):
        for index, row in df.iterrows():
            yield index, row

    def display_bar(self, index, bar):
        """Method for displaying bar data in a tabular format."""
        data_frame = pd.DataFrame.from_records([bar], index=[index])
        data_frame.index.name = "index"  # Add 'index' as the name of the index column
        print(data_frame)

    def on_bar(self, index, bar):
        """Method for handling bar."""

        # Append new tick data to the window
        self.window_data.append(bar["close"])

        # When enough data is available, calculate SMA
        if len(self.window_data) == self.window_size:
            sma = sum(self.window_data) / self.window_size

            # Add the SMA value to your bar data
            bar["SMA"] = sma

        # Print the entire bar
        self.display_bar(index, bar)

    def process_market_data(self):
        """Method for processing data."""
        data_stream = self.simulate_real_time_data(self.data_frame)

        try:
            while True:
                index, data = next(data_stream)
                self.on_bar(index, data)  # or do something with data
        except StopIteration:
            pass

        # for _, row in self.data_frame.iterrows():
        #     timestamp = row["timestamp"]
        #     price = row["price"]
        #     volume = row["volume"]
        #     self.tick_handler.on_tick(timestamp, price, volume)
