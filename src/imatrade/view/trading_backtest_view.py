"""Module for trading backtest view."""


class TradingBacktestView:
    """Class for trading backtest view."""

    # def display_all_backtests(self, backtests):
    #     """Display all backtests."""
    #     print()
    #     print(f"Récapitulatif des backtests, total {len(backtests)} :")
    #     print()
    #     for backtest in backtests:
    #         self.display_backtest_summary(backtest)

    @staticmethod
    def display_all_backtests(backtests):
        """Display all backtests."""
        for backtest_name, backtest in backtests.items():
            print(f"\nBacktest name: {backtest_name}")
            TradingBacktestView.display_backtest(backtest)

    @staticmethod
    def display_backtest(backtest):
        """Display a backtest."""
        print(f"Display name: {backtest.display_name}")
        print(f"Description: {backtest.description}")
        print(f"Strategies: {backtest.strategies}")
        print()
