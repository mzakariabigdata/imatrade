"""
Contient les classes Stategy
"""
import re


def parse_condition(condition_str, data_f):
    """Function to parse a condition string."""
    # Extrayez les noms de colonnes et l'opérateur de la chaîne de condition
    match = re.match(r"([\w\.]+)\s*([<>=]+)\s*([\w\.]+)", condition_str)

    if match is None:
        raise ValueError(f"Could not parse condition string: {condition_str}")
    col1, operation, col2 = match.groups()

    # print(f"Column 1: {col1}", f"Operator: {op}", f"Column 2: {col2}", sep="\n")

    # Récupérez les colonnes du DataFrame
    try:
        # Try to use col1 as a column
        series1 = data_f[col1]
    except KeyError:
        # If that fails, use it as a fixed value
        series1 = float(col1)

    try:
        # Try to use col2 as a column
        series2 = data_f[col2]
    except KeyError:
        # If that fails, use it as a fixed value
        series2 = float(col2)

    # Exécutez l'opération appropriée
    if operation == "<":
        return series1 < series2
    if operation == ">":
        return series1 > series2
    if operation == "==":
        return series1 == series2
    if operation == "<=":
        return series1 <= series2
    if operation == ">=":
        return series1 >= series2
    raise ValueError(f"Unknown operator: {operation}")


class Condition:  # pylint: disable=too-few-public-methods
    """Class for trading conditions."""

    def __init__(self, name, condition):
        self.name = name
        self.condition_str = condition

    def evaluate(self, data):
        """Method to evaluate a condition."""
        # print(f"Evaluating condition: {self.name}", end=" ")
        # print(f"Condition: {self.condition_str}")
        signals = parse_condition(self.condition_str, data)
        return signals


class Rule:  # pylint: disable=too-few-public-methods
    """Class for trading rules."""

    def __init__(self, rule_type, action, conditions):
        self.rule_type = rule_type
        self.action = action
        self.conditions = [Condition(**condition) for condition in conditions]

    def apply(self, data):
        """Method to apply a rule."""
        result_conditions = []
        for condition in self.conditions:
            result = condition.evaluate(data)
            result_conditions.append(result)
            data["C." + condition.name] = result

        data[f"Signal.{self.rule_type}.{self.action}"] = all(result_conditions)
        return data


class RuleSet:  # pylint: disable=too-few-public-methods
    """Class for a set of trading rules."""

    def __init__(self, rule_type, rules):
        self.entry_rule = Rule(rule_type, "entry", rules.get("entry").get("conditions"))
        self.exit_rule = Rule(rule_type, "exit", rules.get("exit").get("conditions"))


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")
        self.instruments = kwargs.get("instruments", [])
        self.quantity = kwargs.get("quantity", 1)

        self.short_rules = RuleSet("short", kwargs.get("short_rules", {}))
        self.long_rules = RuleSet("long", kwargs.get("long_rules", {}))

    def run(self, raw_data):
        """Method to run a trading strategy."""
        data_with_signals = raw_data
        for rule_set in [self.short_rules, self.long_rules]:
            data_with_signals = rule_set.entry_rule.apply(data_with_signals)
            data_with_signals = rule_set.exit_rule.apply(data_with_signals)

        return data_with_signals

    def __repr__(self):
        return f"'Name: {self.name}, Instance of : {type(self).__name__}'"
