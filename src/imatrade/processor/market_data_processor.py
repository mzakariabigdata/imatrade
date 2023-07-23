"""Module for processing market data."""
from datetime import datetime
from collections import deque
import pandas as pd
from src.imatrade.model.tick import Tick


class TradeDetails:  # pylint: disable=too-few-public-methods
    """Represent the trading details of a position"""

    def __init__(self, quantity, entry_price, stop_loss=None, take_profit=None):
        self.quantity = quantity
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.exit_price = None


class Position:  # pylint: disable=too-few-public-methods
    """Represent a position in a trading account"""

    def __init__(self, instrument, position_type, trade_details):
        self.instrument = instrument
        self.position_type = position_type
        self.trade_details = trade_details
        self.entry_time = datetime.now()
        self.exit_time = None
        self.is_open = True
        self.pnl = 0  # "profit_and_loss", "net_gain_loss", "trading_outcome" ou "financial_result"

    def close(self, exit_price):
        """Close the position"""
        if not self.is_open:
            print(f"Position is already closed. Cannot close again {exit_price}.")
            return
        self.is_open = False
        self.exit_time = datetime.now()
        self.trade_details.exit_price = exit_price
        if self.position_type == "long":
            self.pnl = self.trade_details.quantity * (
                self.trade_details.exit_price - self.trade_details.entry_price
            )
        else:  # assuming position_type can be "long" or "short"
            self.pnl = self.trade_details.quantity * (
                self.trade_details.entry_price - self.trade_details.exit_price
            )


class PositionHandler:
    """Class for handling open and close positions."""

    def __init__(self, financial_management):
        self.financial_management = financial_management  # new attribute
        self.open_positions = {}
        self.closed_positions = {}
        self.total_pnl = 0
        self.market_prices = {}
        self.max_drawdown = (
            0  # This should be calculated based on your portfolio value over time
        )

    def get_position_size(self, open_price, stop_loss):
        """Determine the size of the position based on the risk per trade."""
        risk_amount = (
            self.financial_management.get_capital()
            * self.financial_management.risk_per_trade
        )
        print(f"_______stop_loss: {stop_loss} _______open_price: {open_price} _______")
        position_size = risk_amount / abs(open_price - stop_loss)
        return position_size

    def open_position(  # pylint: disable=too-many-arguments
        self,
        instrument,
        position_type,
        open_price,
    ):
        """Method to open a position."""

        # Check if there is already an open position for the instrument
        if instrument in self.open_positions and self.open_positions[instrument]:
            print(f"There is already an open position for {instrument}")
            return

        if self.financial_management.get_stop_loss() is not None:
            # Get the position size based on risk management
            stop_loss = self.financial_management.get_stop_loss()

            quantity = self.get_position_size(open_price, stop_loss)

        take_profit = self.financial_management.get_take_profit()

        invested_amount = quantity * open_price
        self.financial_management.update_capital(-invested_amount)

        trade_details = TradeDetails(quantity, open_price, stop_loss, take_profit)
        position = Position(instrument, position_type, trade_details)
        if instrument not in self.open_positions:
            self.open_positions[instrument] = []
        self.open_positions[instrument].append(position)
        print(
            f"Opened a {position_type} position of {quantity} {instrument} at {open_price}"
        )

    def close_position(self, instrument, position_type, close_price, reason=""):
        """Method to close a position."""
        if instrument not in self.open_positions:
            print(f"No open {position_type} position to close for {instrument}")
            return

        for position in self.open_positions[instrument]:
            if position.position_type == position_type and position.is_open:
                position.close(close_price)
                if instrument not in self.closed_positions:
                    self.closed_positions[instrument] = []
                self.closed_positions[instrument].append(position)
                self.open_positions[instrument].remove(position)
                self.total_pnl += position.pnl
                self.financial_management.close_trade(
                    position.pnl
                )  # Update the financial management parameters
                print(
                    f"Closed a {position_type} position of {position.trade_details.quantity}"
                    f" {instrument} at {close_price} because of {reason}"
                )
                print(
                    f"Updated Financial Management: {self.financial_management}"
                )  # Print out the financial management details
                break
        else:
            print(f"No open {position_type} position to close for {instrument}")

    def update_market_price(self, instrument, bar_data):
        """Update the market price for an instrument."""
        self.market_prices[instrument] = bar_data["close"]
        self.check_stop_loss_and_take_profit(instrument, bar_data)

    def check_stop_loss_and_take_profit(self, instrument, bar_data):
        """Check and execute stop loss and take profit orders for open positions."""
        if instrument not in self.open_positions:
            return

        for position in self.open_positions[instrument]:
            if position.is_open and position.position_type == "long":
                if (
                    position.trade_details.stop_loss is not None
                    and bar_data["low"] <= position.trade_details.stop_loss
                ):
                    self.close_position(
                        instrument,
                        position.position_type,
                        position.trade_details.stop_loss,
                        "stop loss reached",
                    )
                elif (
                    position.trade_details.take_profit is not None
                    and bar_data["high"] >= position.trade_details.take_profit
                ):
                    self.close_position(
                        instrument,
                        position.position_type,
                        position.trade_details.take_profit,
                        "take profit reached",
                    )
            elif position.is_open and position.position_type == "short":
                if (
                    position.trade_details.stop_loss is not None
                    and bar_data["high"] >= position.trade_details.stop_loss
                ):
                    self.close_position(
                        instrument,
                        position.position_type,
                        position.trade_details.stop_loss,
                        "stop loss reached",
                    )
                elif (
                    position.trade_details.take_profit is not None
                    and bar_data["low"] <= position.trade_details.take_profit
                ):
                    self.close_position(
                        instrument,
                        position.position_type,
                        position.trade_details.take_profit,
                        "take profit reached",
                    )

    def get_open_positions(self):
        """Method to get open positions."""
        return self.open_positions

    def get_closed_positions(self):
        """Method to get closed positions."""
        return self.closed_positions

    def total_open_positions(self):
        """Method to get total open positions."""
        total = sum(len(positions) for positions in self.open_positions.values())
        return total


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


class MarketDataProcessor:  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Class for processing market data."""

    def __init__(self, data_frame: pd.DataFrame, strategy=None):
        self.data_frame = data_frame
        self.tick_handler = TickHandler(strategy)
        self.strategy = strategy
        self.num_columns = len(self.data_frame.columns)
        self.indicators = strategy.indicators
        self.data_frame_processed = pd.DataFrame(columns=self.data_frame.columns)
        self.window_data = {
            indicator: deque(maxlen=indicator.get_window_size())
            for indicator in self.indicators
        }
        self.position_handler = PositionHandler(strategy.financial_management)

    def get_data_frame_processed(self):
        """Method for getting data processor."""
        return self.data_frame_processed

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

    def display_bar(self, bar_data, index=None):
        """Method for displaying bar data in a tabular format."""
        data_frame = pd.DataFrame.from_records([bar_data], index=[index])
        data_frame.index.name = "index"  # Add 'index' as the name of the index column
        print(data_frame)

    def apply_startegy(self, bar_data):
        """Method for applying strategy."""
        return self.strategy.run(bar_data)

    def add_indicators(self, bar_data):
        """Method for adding indicators."""

        for indicator, window in self.window_data.items():
            window.append(bar_data["close"])
            if len(window) == indicator.get_window_size():
                indicator_values = indicator.prepare_indicator_data_for_bar(
                    list(window)
                )
                if indicator_values is not None:
                    for key, value in indicator_values.items():
                        bar_data[f"{indicator.name}.{key}"] = value
                else:
                    return None
            else:
                return None
        return bar_data

    def on_bar(self, index, bar_data):
        """Method for handling bar."""

        instrument = self.strategy.instruments[0]
        close_price = bar_data["close"]

        # Update market price for instrument
        self.position_handler.update_market_price(instrument, bar_data)

        bar_data_with_indicator = self.add_indicators(bar_data)
        if bar_data_with_indicator is not None:
            signals_df = self.apply_startegy(bar_data_with_indicator)
            # Vérifier le signal d'achat
            if signals_df["Signal.long.entry"]:
                print(bar_data["time"], end=" ")
                self.position_handler.open_position(instrument, "long", close_price)
            # Vérifier le signal de vente
            elif signals_df["Signal.short.entry"]:
                print(bar_data["time"], end=" ")
                self.position_handler.open_position(instrument, "short", close_price)
            # Vérifier le signal de sortie pour une position longue
            elif signals_df["Signal.long.exit"]:
                print(bar_data["time"], end=" ")
                self.position_handler.close_position(
                    instrument, "long", close_price, "exit signal received"
                )
            # Vérifier le signal de sortie pour une position short
            elif signals_df["Signal.short.exit"]:
                print(bar_data["time"], end=" ")
                self.position_handler.close_position(
                    instrument, "short", close_price, "exit signal received"
                )

            # self.display_bar(signals_df)

        self.add_row_to_dataframe(index, bar_data)
        # self.display_bar(bar_data, index)

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
