"""
Contient les classes Stategy
"""


class Condition:  # pylint: disable=too-few-public-methods
    """Class for trading conditions."""

    def __init__(self, name, condition):
        self.name = name
        self.condition = condition


class Rule:  # pylint: disable=too-few-public-methods
    """Class for trading rules."""

    def __init__(self, action, conditions):
        self.action = action
        self.conditions = [Condition(**condition) for condition in conditions]


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")
        self.entry_rule = Rule(**kwargs.get("rules", [])["entry"])
        self.exit_rule = Rule(**kwargs.get("rules", [])["exit"])

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
