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
        if backtest is None:
            print("Backtest not found !")
            return
        print(f"Display name: {backtest.display_name}")
        print(f"Description: {backtest.description}")
        print(f"Strategies: {backtest.strategies}")
        print()

    @staticmethod
    def display_backtests_summary(backtests):
        """Display a backtests summary."""
        print()
        print(f"Récapitulatif des indicators de trading, total {len(backtests)} :")
        print()
        for _, backtest in backtests.items():
            TradingBacktestView.display_backtest_summary(backtest)

    @staticmethod
    def display_backtest_summary(backtest):
        """Display an backtest summary."""
        print(f"Nom : {backtest.name}")
        print(f"Paramètres : {backtest.strategies}")
        print()