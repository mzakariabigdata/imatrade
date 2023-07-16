"""
Contient les classes Stategy
"""

import pandas as pd


class Condition:  # pylint: disable=too-few-public-methods
    """Class for trading conditions."""

    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def evaluate(self, data):
        """Method to evaluate a condition."""
        print(f"Evaluating condition: {self.name}")
        print(f"Condition: {self.condition}")
        signals = pd.Series(index=data.index, data=False)
        return signals


class Rule:  # pylint: disable=too-few-public-methods
    """Class for trading rules."""

    def __init__(self, action, conditions):
        self.action = action
        self.conditions = [Condition(**condition) for condition in conditions]

    def applay(self, data):
        """Method to applay a rule."""
        print(f"Running rule: {self.action}")
        print(f"Conditions: {self.conditions}")
        # Initialiser un DataFrame de signaux avec des False

        signals = pd.Series(index=data.index, data=False)

        # Évaluer chaque condition
        for condition in self.conditions:
            signals |= condition.evaluate(data)

        return signals


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")
        self.entry_rule = Rule(**kwargs.get("rules", [])["entry"])
        self.exit_rule = Rule(**kwargs.get("rules", [])["exit"])

    def run(self, data):
        """Method to run a trading strategy."""
        print(f"Running strategy: {self.name}")
        print(f"Description: {self.description}")
        print(f"Indicators: {self.indicators}")
        print("data: ", data)
        # Exécuter les règles d'entrée et de sortie
        entry_signals = self.entry_rule.applay(data)
        # print()
        # for indicator in self.indicators:
        #     indicator.run()
        return entry_signals

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"
