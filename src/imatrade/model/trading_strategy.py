"""
Contient les classes Stategy
"""


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")

    def run(self):
        """Method to run a trading strategy."""
        print(f"Running strategy: {self.name}")
        print(f"Description: {self.description}")
        print(f"Indicators: {self.indicators}")
        print()
        for indicator in self.indicators:
            indicator.run()

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"
