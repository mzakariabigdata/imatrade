"""Module for processing market data."""

from collections import deque
import pandas as pd
from src.imatrade.model.tick import Tick


class TickHandler:  # pylint: disable=too-few-public-methods
    """Class for handling ticks."""

    def __init__(self, strategies):
        self.strategies = strategies

    def on_tick(self, **kwargs):
        """Method for handling tick."""
        tick = Tick(**kwargs)

        for strategy in self.strategies:
            strategy.handle_tick(tick)

    def on_bar(  # pylint: disable=too-many-arguments
        self, open_price, high_price, low_price, close_price, volume
    ):
        """Method for handling bar."""
        bar_data = pd.Series(
            index=["open", "high", "low", "close", "volume"],
            data=[open_price, high_price, low_price, close_price, volume],
        )

        for strategy in self.strategies:
            strategy.handle_bar(bar_data)


class MarketDataProcessor:  # pylint: disable=too-few-public-methods
    """Class for processing market data."""

    def __init__(self, data_frame: pd.DataFrame, strategy=None):
        self.data_frame = data_frame
        self.tick_handler = TickHandler(strategy)
        self.indicators = strategy.indicators
        self.data_frame_processed = pd.DataFrame(columns=self.data_frame.columns)
        self.window_data = {
            indicator: deque(maxlen=indicator.get_window_size())
            for indicator in self.indicators
        }

    def add_row_to_dataframe(self, index, row_data):
        """
        Method to add a row of data to the existing dataframe.
        :param row_data: A dictionary containing the data for the new row.
        """
        # Get missing columns
        missing_columns = set(row_data.keys()) - set(self.data_frame_processed.columns)

        # Concatenate data frames to add missing columns
        if missing_columns:
            missing_data = pd.DataFrame(columns=list(missing_columns))
            self.data_frame_processed = pd.concat(
                [self.data_frame_processed, missing_data], axis=1
            )

        # Append row to the data frame
        self.data_frame_processed.loc[index] = row_data

    def set_data_frame(self, data_frame):
        """Method for setting data frame."""
        self.data_frame = data_frame

    def simulate_real_time_data(self, data_frame: pd.DataFrame):
        """Method for simulating real time data."""
        for index, row in data_frame.iterrows():
            yield index, row

    def display_bar(self, index, bar_data):
        """Method for displaying bar data in a tabular format."""
        data_frame = pd.DataFrame.from_records([bar_data], index=[index])
        data_frame.index.name = "index"  # Add 'index' as the name of the index column
        print(data_frame)

    def on_bar(self, index, bar_data):
        """Method for handling bar."""

        # Append new tick data to each window
        for indicator, window in self.window_data.items():
            window.append(bar_data["close"])
            if len(window) == indicator.get_window_size():
                indicator_values = indicator.prepare_indicator_data_for_bar(
                    list(window)
                )
                if indicator_values is not None:
                    for key, value in indicator_values.items():
                        bar_data[f"{indicator.name}_{key}"] = value
        self.add_row_to_dataframe(index, bar_data)
        # Print the entire bar
        self.display_bar(index, bar_data)

    def process_market_data(self):
        """Method for processing data."""
        data_stream = self.simulate_real_time_data(self.data_frame)

        try:
            while True:
                index, data = next(data_stream)
                self.on_bar(index, data)  # or do something with data
        except StopIteration:
            pass

        print(self.data_frame_processed.dropna())
        # for _, row in self.data_frame.iterrows():
        #     timestamp = row["timestamp"]
        #     price = row["price"]
        #     volume = row["volume"]
        #     self.tick_handler.on_tick(timestamp, price, volume)
