"""Module for the trading strategy view."""

import io
import sys


def test_display_all_strategies(trading_strategy_controller):
    """Test hello world."""

    # Create a temporary variable to replace stdout
    temp_out = io.StringIO()
    # Replace stdout with our temporary variable
    sys.stdout = temp_out
    # Run the function we want to test
    trading_strategy_controller.create_all_strategies()
    trading_strategy_controller.display_all_strategies()
    # Replace stdout with its original value
    sys.stdout = sys.__stdout__
    # Now temp_out.getvalue() contains whatever would have been printed by the function
    output = temp_out.getvalue()

    # You can now make assertions about the contents of output
    assert "Stratégies de trading" in output
