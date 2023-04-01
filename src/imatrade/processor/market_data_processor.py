import pandas as pd
from imatrade.model.tick import Tick

class TickHandler:
    def __init__(self, strategies):
        self.strategies = strategies

    def on_tick(self, timestamp, price, volume):
        tick = Tick(timestamp, price, volume)

        for strategy in self.strategies:
            strategy.handle_tick(tick)
            

class MarketDataProcessor:
    def __init__(self, data_frame: pd.DataFrame, strategies):
        self.data_frame = data_frame
        self.tick_handler = TickHandler(strategies)

    def process_data(self):
        for index, row in self.data_frame.iterrows():
            timestamp = row['timestamp']
            price = row['price']
            volume = row['volume']
            self.tick_handler.on_tick(timestamp, price, volume)
