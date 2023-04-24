"""Tick class definition."""


class Tick:
    def __init__(self, timestamp, price, volume):
        self.timestamp = timestamp
        self.price = price
        self.volume = volume

    def __str__(self):
        return f"Tick({self.timestamp}, {self.price}, {self.volume})"

    def __repr__(self):
        return self.__str__()
