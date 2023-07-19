"""
Contient les classes Stategy
"""

import pandas as pd


class Condition:  # pylint: disable=too-few-public-methods
    """Class for trading conditions."""

    def __init__(self, name, condition):
        self.name = name
        self.condition_str = condition

    def evaluate(self, data):
        """Method to evaluate a condition."""
        print(f"Evaluating condition: {self.name}")
        print(f"Condition: {self.condition_str}")
        # Ajouter cette ligne pour récupérer la valeur de BollingerBands_hband et close
        print("_____________data: ", data)
        bollinger_hband = data["BollingerBands_hband"]
        print("__________________bollinger_hband: ", bollinger_hband)
        # close = data['close']

        # Ajouter cette ligne pour évaluer la condition
        # condition_result = pd.eval(self.condition_str, engine='python', local_dict=data)

        # # condition_result = eval(self.condition_str, {'BollingerBands_hband': bollinger_hband, 'close': close})
        # print("condition_result: ", condition_result)
        # # signals = pd.Series(index=data.index, data=False)
        # # return signals
        # return condition_result


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

        # signals = pd.Series(index=data.index, data=False)
        print("nnnnnnnnnnnnnnndata: ", data)
        for condition in self.conditions:
            condition.evaluate(data)

        # Évaluer chaque condition
        # for condition in self.conditions:
        #     signals |= condition.evaluate(data)
        # print("signals: ", signals)

        # return signals


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")
        self.entry_rule = Rule(**kwargs.get("rules", [])["entry"])
        self.exit_rule = Rule(**kwargs.get("rules", [])["exit"])

    def run(self, raw_data):
        """Method to run a trading strategy."""
        print(f"Running strategy: {self.name}")
        print(f"Description: {self.description}")
        print(f"Indicators: {self.indicators}")
        print("44444444444444data: ", raw_data)
        # Exécuter les règles d'entrée et de sortie
        # entry_signals = self.entry_rule.applay(raw_data) # bizarre
        # print()
        # for indicator in self.indicators:
        #     indicator.run()
        # return entry_signals

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"
