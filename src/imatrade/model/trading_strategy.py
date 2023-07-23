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


class FinancialManagement:  # pylint: disable=too-many-instance-attributes
    """Represent the financial parameters of a trading strategy"""

    def __init__(self, initial_capital, risk_per_trade, stop_loss, take_profit):
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.initial_capital = initial_capital
        self.current_capital = (
            initial_capital  # suppose que nous commençons avec le capital initial
        )
        self.risk_per_trade = risk_per_trade
        self.pnl = 0
        self.trades = 0
        self.win_trades = 0
        self.loss_trades = 0

    def get_take_profit(self):
        """Return the take profit value"""
        return self.take_profit

    def display(self):
        """Display the financial management details"""
        print("Financial Management Details:")
        print(f"Initial capital: {self.initial_capital}")
        print(f"Current capital: {self.current_capital}")
        print(f"Risk per trade: {self.risk_per_trade}")
        print(f"Total PnL: {self.pnl}")
        print(f"Total trades: {self.trades}")
        print(f"Winning trades: {self.win_trades}")
        print(f"Losing trades: {self.loss_trades}")
        print(f"Stop loss: {self.stop_loss}")
        print(f"Take profit: {self.take_profit}")

    def get_stop_loss(self):
        """Return the stop loss value"""
        return self.stop_loss

    def close_trade(self, pnl):
        """Close a trade and update the financial management parameters."""
        self.update_capital(pnl)
        self.trades += 1
        self.pnl += pnl
        if pnl > 0:
            self.win_trades += 1
        elif pnl < 0:
            self.loss_trades += 1

    def update_capital(self, pnl):
        """Update the current capital based on profit or loss from a trade"""
        self.current_capital += pnl

    def calculate_position_size(self):
        """Calculate the position size based on risk per trade and current capital"""
        return self.current_capital * self.risk_per_trade

    def calculate_performance(self):
        """Calculate performance metrics"""
        # TODO: Implement performance calculations

    def get_capital(self):
        """Return the current capital."""
        return self.current_capital

    def get_current_capital(self):
        """Return the current capital."""
        return self.current_capital

    def __repr__(self):
        # return all the parameters of the financial management
        return (
            f"Initial capital: {self.initial_capital}, Current capital: {self.current_capital},"
            f"Risk per trade: {self.risk_per_trade}, PnL: {self.pnl}, Trades: {self.trades}, "
            f"Win trades: {self.win_trades}, Loss trades: {self.loss_trades}"
        )


class TradingStrategy:
    """Class for trading strategies."""

    def __init__(self, **kwargs):
        self.indicators = kwargs.get("indicators", [])
        self.name = kwargs.get("name", "Default Trading Strategy")
        self.description = kwargs.get("description", "Default Trading Strategy")
        self.instruments = kwargs.get("instruments", [])
        self.financial_management = FinancialManagement(
            kwargs.get("financial_management").get("initial_capital"),
            kwargs.get("financial_management").get("risk_per_trade"),
            kwargs.get("financial_management").get("stop_loss"),
            kwargs.get("financial_management").get("take_profit"),
        )
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
